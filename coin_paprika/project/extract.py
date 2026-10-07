import requests
from decouple import config, Csv

coins = config('COINS',default='xrp-xrp',cast=Csv())
url = "https://api.coinpaprika.com/v1/tickers"

def extract_data():
    try:
        print(f"Getting data from coinpaprika API")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("Error: request timed out.")
        return []
    except requests.exceptions.ConnectionError:
        print("Error: failed to connect to coinpaprika API.")
        return []
    except requests.exceptions.HTTPError as http_err:
        print(f"Error: HTTP error occurred: {http_err}")
        return []
    except requests.exceptions.RequestException as req_err:
        print(f"Error: an error occurred while requesting data: {req_err}")
        return []

    try:
        all_data = response.json()
    except ValueError as json_err:
        print(f"Error: failed to parse JSON response: {json_err}")
        return []

    if not isinstance(all_data, list):
        print("Error: unexpected response format from API (expected a list).")
        return []

    filtered_data = [item for item in all_data if item.get("id") in coins]

    found_ids = {item.get("id") for item in filtered_data}
    missing_coins = set(coins) - found_ids
    if missing_coins:
        print(f"Warning: could not find data for coins: {missing_coins}")

    print(f"Successfully extracted data for {len(filtered_data)} coin(s).")
    return filtered_data


if __name__ == "__main__":
    data = extract_data()