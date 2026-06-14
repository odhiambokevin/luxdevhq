from decouple import config
from sqlalchemy import create_engine,text
from extract import extract_data

#database connection string variables set from .env file
DB_HOST = config('DB_HOST',default='localhost')
DB_PORT = config('DB_PORT',default='5432')
DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
STAGING_SCHEMA = config('STAGING_SCHEMA')

conn_string = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(conn_string)

def load_data(dataframe):
    print(f"\npreparing to send data to database...")
    #create specific schema
    staging_schema = STAGING_SCHEMA
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {staging_schema};"))
        conn.commit()
    
    dataframe.to_sql('gas_prices', engine, if_exists='replace',schema=staging_schema, index=False)
    print(f"Data sent to database successfully!")