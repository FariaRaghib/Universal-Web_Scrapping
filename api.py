import requests
import pandas as pd

def fetch_api(url, api_key=None, params=None):
    try:
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        df = None
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.DataFrame([data])

        return {"success": True, "json": data, "table": df}
    except Exception as e:
        return {"success": False, "error": str(e), "json": None, "table": None}


# Example usage for CoinGecko API
if __name__ == "__main__":
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "per_page": 5, "page": 1}
    result = fetch_api(url, params=params)
    print(result["table"])
