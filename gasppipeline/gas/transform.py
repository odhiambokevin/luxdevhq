import json
import pandas as pd

def drop_col(raw_data):
    json_data = json.loads(raw_data.decode("utf-8"))
    cities_data = json_data["result"]["cities"]

    citiesdf = pd.DataFrame(cities_data)

    #drop lowername columns
    citiesdf.drop(columns=['lowername'], inplace=True)
    print(f"\nsuccessfully dropped columns")
    return citiesdf

def rename_df(dataframe):
    #rename 'name' column
    dataframe.rename(columns={'name':'city'},inplace=True)

    print(f"\nsuccessfully renamed columns")
    return dataframe

