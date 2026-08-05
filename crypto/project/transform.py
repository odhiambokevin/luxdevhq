import pandas as pd

OUTPUT_COLUMNS = ["id", "name", "symbol", "price"]


def transform_data(data):
    if not data:
        print("Warning: no data received for transformation. Returning empty data frame.")
        return []

    try:
        df = pd.DataFrame(data)
    except Exception as e:
        print(f"Error: failed to convert data to DataFrame: {e}")
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    required_columns = {"id", "name", "symbol", "quotes"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        print(f"Error: missing expected column(s) in data: {missing_columns}")
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    def _get_usd_price(quotes):
        try:
            if isinstance(quotes, dict):
                return quotes.get("USD", {}).get("price")
        except AttributeError:
            pass
        return None

    try:
        df["price"] = df["quotes"].apply(_get_usd_price)
    except Exception as e:
        print(f"Error: failed to extract USD price from quotes: {e}")
        df["price"] = None

    # Drop all columns except the ones we need
    try:
        df = df[OUTPUT_COLUMNS]
    except KeyError as e:
        print(f"Error: expected output columns not found after transform: {e}")
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    missing_price_count = int(df["price"].isna().sum())
    if missing_price_count:
        print(f"Warning: {missing_price_count} row(s) missing USD price data.")

    print(f"Transformation complete. {len(df)} row(s) produced.")
    return df


if __name__ == "__main__":
    from extract import extract_data

    raw_data = extract_data()
    transformed_df = transform_data(raw_data)
    print(transformed_df.to_string(index=False))