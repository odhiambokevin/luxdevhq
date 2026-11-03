from datetime import date
from pathlib import Path

import polars as pl

REQUIRED_COLUMNS = (
    "date", "admin1", "admin2", "market", "market_id", "latitude", "longitude",
    "category", "commodity", "commodity_id", "unit", "priceflag", "pricetype",
    "currency", "price", "usdprice",
)
CLEAN_COLUMNS = (
    "obs_date", "month_start", "market_id", "market_name", "admin1", "admin2",
    "county_code", "latitude", "longitude", "commodity_id", "unit_code",
    "price_type", "price_flag", "currency", "price", "price_usd",
    "price_per_base", "base_unit", "unit_convertible",
)
NATURAL_KEY = ("obs_date", "market_id", "commodity_id", "unit_code", "price_type")
CPI_OVERALL_COLUMNS = (
    "report_date", "overall_cpi", "mom_change", "yoy_inflation", "core_inflation", "non_core_inflation",
)
CPI_DIVISION_COLUMNS = ("report_date", "division_name", "weight", "division_mom", "division_yoy")
MONTH_START = pl.date(pl.col("obs_date").dt.year(), pl.col("obs_date").dt.month(), 1)


def read_seeds(seeds_dir: Path) -> dict[str, pl.DataFrame]:
    return {
        "counties": pl.read_csv(seeds_dir / "counties.csv"),
        "admin2_map": pl.read_csv(seeds_dir / "admin2_county_map.csv"),
        "market_override": pl.read_csv(seeds_dir / "market_county_override.csv").rename(
            {"county_name": "override_county"}
        ),
        "commodities": pl.read_csv(seeds_dir / "commodity_map.csv"),
        "units": pl.read_csv(seeds_dir / "units.csv"),
    }


def read_prices(path: Path) -> pl.DataFrame:
    raw = pl.read_csv(path, infer_schema_length=0)
    missing = [column for column in REQUIRED_COLUMNS if column not in raw.columns]
    if missing:
        raise ValueError(f"source file is missing required columns: {missing}")
    return raw.filter(~pl.col("date").str.starts_with("#"))


def type_prices(raw: pl.DataFrame) -> pl.DataFrame:
    return raw.with_columns(
        pl.col("date").str.to_date("%Y-%m-%d", strict=False).alias("obs_date"),
        pl.col("market_id").cast(pl.Int64, strict=False),
        pl.col("commodity_id").cast(pl.Int64, strict=False),
        pl.col("latitude").cast(pl.Float64, strict=False),
        pl.col("longitude").cast(pl.Float64, strict=False),
        pl.col("price").cast(pl.Float64, strict=False),
        pl.col("usdprice").cast(pl.Float64, strict=False),
    ).with_columns(MONTH_START.alias("month_start"))


def reject_reason() -> pl.Expr:
    return (
        pl.when(pl.col("obs_date").is_null()).then(pl.lit("invalid_date"))
        .when(pl.col("market_id").is_null() | pl.col("commodity_id").is_null()).then(pl.lit("invalid_key"))
        .when(pl.col("currency") != "KES").then(pl.lit("unsupported_currency"))
        .when(pl.col("price").is_null() | (pl.col("price") <= 0)).then(pl.lit("invalid_price"))
        .when(pl.col("county_code").is_null()).then(pl.lit("unmapped_county"))
        .when(pl.col("commodity_group").is_null()).then(pl.lit("unknown_commodity"))
        .when(pl.col("base_unit").is_null()).then(pl.lit("unknown_unit"))
        .otherwise(pl.lit(None, dtype=pl.String))
        .alias("reject_reason")
    )


def enrich(typed: pl.DataFrame, seeds: dict[str, pl.DataFrame]) -> pl.DataFrame:
    commodities = seeds["commodities"].select("commodity_id", "commodity_group", "is_food", "is_staple")
    units = seeds["units"].rename({"unit": "unit_seed"})
    return (
        typed.join(seeds["admin2_map"], on="admin2", how="left")
        .join(seeds["market_override"], on="market_id", how="left")
        .with_columns(pl.coalesce("county_name", "override_county").alias("county_name"))
        .join(seeds["counties"].select("county_code", "county_name"), on="county_name", how="left")
        .join(commodities, on="commodity_id", how="left")
        .join(units, left_on="unit", right_on="unit_seed", how="left")
        .with_columns(
            (pl.col("quantity").is_not_null() & (pl.col("base_unit") != "none")).alias("unit_convertible"),
            pl.when(pl.col("quantity").is_not_null() & (pl.col("base_unit") != "none"))
            .then(pl.col("price") / pl.col("quantity"))
            .otherwise(None)
            .alias("price_per_base"),
        )
        .with_columns(reject_reason())
    )


def clean_prices(raw: pl.DataFrame, month: date, seeds: dict[str, pl.DataFrame]) -> tuple[pl.DataFrame, pl.DataFrame]:
    enriched = enrich(type_prices(raw).filter(pl.col("month_start") == month), seeds)
    rejected = enriched.filter(pl.col("reject_reason").is_not_null()).select(
        pl.col("month_start"),
        pl.col("reject_reason"),
        pl.struct([pl.col(name) for name in REQUIRED_COLUMNS]).struct.json_encode().alias("raw_json"),
    )
    clean = (
        enriched.filter(pl.col("reject_reason").is_null())
        .rename({"market": "market_name", "unit": "unit_code", "pricetype": "price_type",
                 "priceflag": "price_flag", "usdprice": "price_usd"})
        .select(CLEAN_COLUMNS)
    )
    return clean, rejected


def source_profile(raw: pl.DataFrame) -> dict[str, object]:
    typed = type_prices(raw)
    return {
        "rows": typed.height,
        "invalid_dates": typed.filter(pl.col("obs_date").is_null()).height,
        "max_month": typed["month_start"].max(),
    }


def read_cpi(overall_path: Path, division_path: Path) -> tuple[pl.DataFrame, pl.DataFrame]:
    overall = pl.read_csv(overall_path, try_parse_dates=True).select(CPI_OVERALL_COLUMNS)
    division = pl.read_csv(division_path, try_parse_dates=True).select(CPI_DIVISION_COLUMNS)
    return overall, division
