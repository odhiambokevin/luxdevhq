import sys
from pathlib import Path

import polars as pl

from foodprices.transform import read_prices, type_prices

DEFAULT_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "wfp_food_prices_ken.csv"


def main(path: Path) -> None:
    typed = type_prices(read_prices(path))
    print(f"file: {path}")
    print(f"rows: {typed.height}, markets: {typed['market_id'].n_unique()}, commodities: {typed['commodity_id'].n_unique()}")
    print(f"date range: {typed['obs_date'].min()} to {typed['obs_date'].max()}, unparseable dates: {typed['obs_date'].null_count()}")
    print("null counts:")
    print(typed.null_count().transpose(include_header=True, column_names=["nulls"]).filter(pl.col("nulls") > 0))
    for column in ("admin1", "pricetype", "priceflag", "currency", "unit", "category"):
        print(f"\n{column}:")
        print(typed.group_by(column).len().sort("len", descending=True))
    print("\nrows per year:")
    print(typed.group_by(pl.col("obs_date").dt.year().alias("year")).len().sort("year"))
    print("\nretail markets per year:")
    print(
        typed.filter(pl.col("pricetype") == "Retail")
        .group_by(pl.col("obs_date").dt.year().alias("year"))
        .agg(pl.col("market_id").n_unique().alias("markets"))
        .sort("year")
    )
    duplicates = typed.select("obs_date", "market_id", "commodity_id", "unit", "pricetype").is_duplicated().sum()
    print(f"\nduplicate natural keys: {duplicates}")
    print(f"non-positive prices: {typed.filter(pl.col('price') <= 0).height}")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH)
