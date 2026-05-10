# Python Pandas Assignement

## 1. Dummy Json Data

The challenge for this was that some columns retrieved from the API had nested dictionary and strings inside them.

For the `Products` API, a simple `pandas.json_normalize() would flatten out the data so that all nested dictionaries are in one flat table.

The `carts` data was a bit more complicated since it has several layers of nested data and some were string fro which the `pd.json_normalize()` would not directly work.

I first examine the first normalized table with the code:
```bash
carts_df = pd.json_normalize(carts_df_raw['carts'])
```
I identify the `products` column as having nested list of dictionaries. I then put all the `product` items into their own table:
```bash
products_normalized = pd.json_normalize(df_exploded['products'])
```
Finally I merge them back to the first level normalized database but drop the `products` column from the first normalized database.
```bash
final_df = pd.concat([df_exploded.drop(columns=['products']), products_normalized], axis=1)
```

I then export both dataframes ie products and carts to a csv.