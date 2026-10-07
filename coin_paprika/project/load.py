import pandas as pd
from decouple import UndefinedValueError, config
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# --- Database connection variables, set from .env file ---
try:
   #database connection string variables set from .env file
    DB_HOST = config('DB_HOST',default='localhost')
    DB_PORT = config('DB_PORT',default='5432')
    DB_NAME = config('DB_NAME')
    DB_USER = config('DB_USER')
    DB_PASSWORD = config('DB_PASSWORD')
    STAGING_SCHEMA = config('STAGING_SCHEMA')
except UndefinedValueError as e:
    print(f"Error: missing required environment variable: {e}")
    raise

conn_string = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(conn_string)

def load_data(dataframe, table_name="crypto_prices"):
    if dataframe is None or dataframe.empty:
        print("Warning: no data to load. Skipping database load...")
        return False

    print("\npreparing to send data to database...")

    #create schema if it doesn't exist
    try:
        with engine.connect() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {STAGING_SCHEMA};"))
            conn.commit()
    except SQLAlchemyError as e:
        print(f"Error: failed to create schema '{STAGING_SCHEMA}': {e}")
        return False

    #upload the dataframe into the database table
    try:
        dataframe.to_sql(table_name,engine,if_exists="replace",schema=STAGING_SCHEMA,index=False,)
    except SQLAlchemyError as e:
        print(f"Error: failed to load data into table '{table_name}': {e}")
        return False
    except ValueError as e:
        print(f"Error: invalid data for insertion into '{table_name}': {e}")
        return False

    print("Data sent to database successfully!")
    return True


if __name__ == "__main__":
    sample_df = pd.DataFrame(
        [{"id": "btc-bitcoin", "name": "Bitcoin", "symbol": "BTC", "price": 5162.15}]
    )
    load_data(sample_df)