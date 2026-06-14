import http.client

from decouple import config

def extract_data():
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        'content-type': "application/json",
        'authorization': config('API_KEY'),
        }
    
    try:
        print(f"getting data from API...")
        conn.request("GET", "/gasPrice/stateUsaPrice?state=WA", headers=headers)
        res = conn.getresponse()
        data = res.read()
        print("\ndata extracted successfully!")
        return data
    
    except Exception as e:
        return f"\nAn error occured: {e}"
    finally:
        conn.close()