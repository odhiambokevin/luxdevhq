"""Monthly batch load of Kenyan food prices and KNBS CPI into the PostgreSQL star schema."""

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import polars as pl
from airflow.sdk import dag, task

from foodprices import extract, load, quality, transform
from foodprices.config import DAG_ID, get_settings

try:
    from airflow.sdk.exceptions import AirflowFailException
except ImportError:
    from airflow.exceptions import AirflowFailException

MONTH = "{{ data_interval_start | ds }}"
MONTH_END = "{{ data_interval_end | ds }}"
RUN_ID = "{{ run_id }}"

DEFAULT_ARGS = {
    "owner": "kevin.odhiambo",
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=30),
    "execution_timeout": timedelta(minutes=20),
}


def record_failure(context: dict[str, Any]) -> None:
    dag_run = context["dag_run"]
    load.record_run_status(
        get_settings(),
        dag_run.run_id,
        dag_run.data_interval_start.date(),
        "failed",
        {"reason": str(context.get("reason"))},
    )


@dag(
    dag_id=DAG_ID,
    schedule="@monthly",
    start_date=datetime(2015, 1, 1),
    catchup=True,
    max_active_runs=1,
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(hours=2),
    on_failure_callback=record_failure,
    tags=["food-prices", "kenya", "batch"],
    doc_md=__doc__,
)
def food_prices_load_monthly() -> None:
    @task
    def extract_prices() -> dict[str, Any]:
        settings = get_settings()
        snapshot = extract.snapshot_prices(settings)
        load.register_snapshot(settings, snapshot)
        return snapshot

    @task
    def extract_cpi() -> dict[str, Any]:
        settings = get_settings()
        snapshots = extract.snapshot_cpi(settings)
        for snapshot in snapshots.values():
            load.register_snapshot(settings, snapshot)
        return snapshots

    @task
    def clean_prices(snapshot: dict[str, Any], month: str) -> dict[str, Any]:
        settings = get_settings()
        month_start = date.fromisoformat(month)
        raw = transform.read_prices(Path(snapshot["snapshot_path"]))
        clean, rejected = transform.clean_prices(raw, month_start, transform.read_seeds(settings.seeds_dir))
        target = settings.processed_dir / month_start.strftime("%Y-%m")
        target.mkdir(parents=True, exist_ok=True)
        clean.write_parquet(target / "prices_clean.parquet")
        rejected.write_parquet(target / "prices_rejected.parquet")
        profile = transform.source_profile(raw)
        return {
            "sha256": snapshot["sha256"],
            "clean_path": str(target / "prices_clean.parquet"),
            "rejected_path": str(target / "prices_rejected.parquet"),
            "rows_clean": clean.height,
            "rows_rejected": rejected.height,
            "invalid_dates": profile["invalid_dates"],
            "source_max_month": str(profile["max_month"]),
        }

    @task
    def validate_prices(cleaned: dict[str, Any], month: str) -> dict[str, Any]:
        month_start = date.fromisoformat(month)
        profile = {
            "invalid_dates": cleaned["invalid_dates"],
            "max_month": date.fromisoformat(cleaned["source_max_month"]),
        }
        results = quality.validate_prices(
            pl.read_parquet(cleaned["clean_path"]),
            pl.read_parquet(cleaned["rejected_path"]),
            profile,
            month_start,
        )
        load.write_validation_results(get_settings(), month_start, "pre_load", results)
        failed = quality.failed_errors(results)
        if failed:
            raise AirflowFailException(f"validation failed: {[result.name for result in failed]}")
        return cleaned

    @task
    def stage_prices(validated: dict[str, Any], month: str, run_id: str) -> dict[str, Any]:
        load.stage_prices(
            get_settings(),
            pl.read_parquet(validated["clean_path"]),
            pl.read_parquet(validated["rejected_path"]),
            date.fromisoformat(month),
            run_id,
            validated["sha256"],
        )
        return validated

    @task
    def load_dimensions(staged: dict[str, Any], month: str) -> dict[str, Any]:
        load.load_dimensions(get_settings(), date.fromisoformat(month))
        return staged

    @task
    def load_facts(dimensions: dict[str, Any], month: str) -> dict[str, Any]:
        rows_loaded = load.load_facts(get_settings(), date.fromisoformat(month))
        return {**dimensions, "rows_loaded": rows_loaded}

    @task
    def build_inflation(facts: dict[str, Any], month: str) -> dict[str, Any]:
        load.build_inflation(get_settings(), date.fromisoformat(month))
        return facts

    @task
    def load_cpi(snapshots: dict[str, Any], month: str, run_id: str) -> dict[str, Any]:
        settings = get_settings()
        overall, division = transform.read_cpi(
            Path(snapshots["overall"]["snapshot_path"]),
            Path(snapshots["division"]["snapshot_path"]),
        )
        return load.load_cpi(
            settings, overall, division, date.fromisoformat(month), run_id, snapshots["overall"]["sha256"]
        )

    @task
    def check_warehouse(inflation: dict[str, Any], cpi: dict[str, Any], month: str) -> dict[str, Any]:
        settings = get_settings()
        month_start = date.fromisoformat(month)
        results = load.reconcile_month(
            settings,
            month_start,
            expected_clean=inflation["rows_clean"],
            expected_total=inflation["rows_clean"] + inflation["rows_rejected"],
        )
        load.write_validation_results(settings, month_start, "post_load", results)
        failed = quality.failed_errors(results)
        if failed:
            raise AirflowFailException(f"reconciliation failed: {[result.name for result in failed]}")
        return {**inflation, **cpi}

    @task
    def record_run(checked: dict[str, Any], month: str, month_end: str, run_id: str) -> None:
        load.record_run_status(
            get_settings(),
            run_id,
            date.fromisoformat(month),
            "success",
            {key: checked[key] for key in ("cpi_overall_rows", "cpi_division_rows", "source_max_month")},
            data_interval_end=date.fromisoformat(month_end),
            sha256=checked["sha256"],
            rows_read=checked["rows_clean"] + checked["rows_rejected"],
            rows_loaded=checked["rows_loaded"],
            rows_rejected=checked["rows_rejected"],
        )

    cleaned = clean_prices(extract_prices(), MONTH)
    validated = validate_prices(cleaned, MONTH)
    staged = stage_prices(validated, MONTH, RUN_ID)
    dimensions = load_dimensions(staged, MONTH)
    facts = load_facts(dimensions, MONTH)
    inflation = build_inflation(facts, MONTH)
    cpi = load_cpi(extract_cpi(), MONTH, RUN_ID)
    checked = check_warehouse(inflation, cpi, MONTH)
    record_run(checked, MONTH, MONTH_END, RUN_ID)


food_prices_load_monthly()
