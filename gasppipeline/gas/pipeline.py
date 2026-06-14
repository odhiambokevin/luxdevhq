import http.client
import json

import pandas as pd
from decouple import config
from sqlalchemy import create_engine,text

#database connection string variables set from .env file
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
STAGING_SCHEMA = config('STAGING_SCHEMA')

conn = http.client.HTTPSConnection("api.collectapi.com")

headers = {
    'content-type': "application/json",
    'authorization': "apikey 5OPjj8xLOygjpPa4Rq7pcr:50NQ3rwuf8WZdwtgUrYPon"
    }

conn.request("GET", "/gasPrice/stateUsaPrice?state=WA", headers=headers)

res = conn.getresponse()
data = res.read()

#get the data into python dictionary
json_gasdata = json.loads(data.decode("utf-8"))
cities_data = json_gasdata["result"]["cities"]

citiesdf = pd.DataFrame(cities_data)

#drop lowername columns
citiesdf.drop(columns=['lowername'], inplace=True)

#rename 'name' column
citiesdf.rename(columns={'name':'city'},inplace=True)

#connect to and from database using sqlalchemy and psycopg2
conn_string = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(conn_string)

#create specific schema
staging_schema = STAGING_SCHEMA
with engine.connect() as conn:
    conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {staging_schema};"))
    conn.commit()

citiesdf.to_sql('gas_prices', engine, if_exists='replace',schema=staging_schema, index=False)