import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_html(url: str):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Find all tables manually
        tables = soup.find_all("table")

        if not tables:
            return {"success": False, "error": "No tables found on the page", "table": None, "raw": None}

        # Convert all tables into Pandas DataFrames
        dfs = []
        for table in tables:
            try:
                df = pd.read_html(str(table))[0]
                dfs.append(df)
            except:
                continue

        if dfs:
            # Return the first table (or merge later if you want multiple)
            return {"success": True, "table": dfs[0], "raw": None, "error": None}
        else:
            return {"success": False, "error": "Tables detected but could not be parsed", "table": None, "raw": None}

    except Exception as e:
        return {"success": False, "error": str(e), "table": None, "raw": None}
