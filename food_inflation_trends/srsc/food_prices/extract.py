import hashlib
import shutil
import urllib.request
from pathlib import Path
from typing import Any

from foodprices.config import CPI_SOURCE_CODE, WFP_SOURCE_CODE, Settings

CPI_FILES = {"overall": "monthly_trend.csv", "division": "master_analysis.csv"}
USER_AGENT = "kenya-food-prices-pipeline/1.0"


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, destination: Path) -> Path:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    partial = destination.with_suffix(destination.suffix + ".part")
    with urllib.request.urlopen(request, timeout=120) as response, partial.open("wb") as out:
        shutil.copyfileobj(response, out)
    partial.replace(destination)
    return destination


def snapshot_file(source: Path, snapshot_dir: Path, source_code: str) -> dict[str, Any]:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    digest = sha256_of(source)
    target = snapshot_dir / f"{source.stem}_{digest[:16]}{source.suffix}"
    if not target.exists():
        shutil.copy2(source, target)
    return {
        "source_code": source_code,
        "sha256": digest,
        "file_name": source.name,
        "size_bytes": target.stat().st_size,
        "snapshot_path": str(target),
    }


def snapshot_prices(settings: Settings) -> dict[str, Any]:
    settings.snapshot_dir.mkdir(parents=True, exist_ok=True)
    if settings.wfp_source_url:
        landed = download(settings.wfp_source_url, settings.snapshot_dir / "wfp_food_prices_ken.download.csv")
        snapshot = snapshot_file(landed, settings.snapshot_dir, WFP_SOURCE_CODE)
        landed.unlink()
        snapshot["file_name"] = "wfp_food_prices_ken.csv"
        return snapshot
    return snapshot_file(settings.wfp_local_path, settings.snapshot_dir, WFP_SOURCE_CODE)


def snapshot_cpi(settings: Settings) -> dict[str, Any]:
    return {
        kind: snapshot_file(settings.cpi_dir / name, settings.snapshot_dir, CPI_SOURCE_CODE)
        for kind, name in CPI_FILES.items()
    }
