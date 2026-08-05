import sys

from extract import extract_data
from load import load_data
from transform import transform_data

def run_pipeline():
    print("Starting crypto ETL pipeline...")

    # --- Step 1: Extract ---
    try:
        raw_data = extract_data()
    except Exception as e:
        print(f"Error: unexpected error during extraction: {e}")
        sys.exit(1)

    if not raw_data:
        print("Error: no data extracted. Aborting pipeline.")
        sys.exit(1)

    # --- Step 2: Transform ---
    try:
        transformed_df = transform_data(raw_data)
    except Exception as e:
        print(f"Error: unexpected error during transformation: {e}")
        sys.exit(1)

    if transformed_df.empty:
        print("Error: transformation produced no data. Aborting pipeline.")
        sys.exit(1)

    # --- Step 3: Load ---
    try:
        success = load_data(transformed_df)
    except Exception as e:
        print(f"Error: unexpected error during load: {e}")
        sys.exit(1)

    if not success:
        print("Error: pipeline finished with errors during the load step.")
        sys.exit(1)

    print("Pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()