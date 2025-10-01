import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_html(url: str):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        tables = soup.find_all("table")
        if not tables:
            return {"success": False, "error": "No tables found", "table": None, "raw": None}

        all_dfs = []

        for table in tables:
            headers = []
            rows = []

            # Extract headers
            header_row = table.find("thead")
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all("th")]

            # Extract rows
            body_rows = table.find_all("tr")
            for tr in body_rows:
                cols = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                if cols:
                    rows.append(cols)

            # Build DataFrame
            if headers and rows:
                df = pd.DataFrame(rows, columns=headers[:len(rows[0])])
            else:
                df = pd.DataFrame(rows)

            if not df.empty:
                all_dfs.append(df)

        if all_dfs:
            # Return the first table (could extend to all)
            return {"success": True, "table": all_dfs[0], "raw": None, "error": None}
        else:
            return {"success": False, "error": "Tables found but empty after parsing", "table": None, "raw": None}

    except Exception as e:
        return {"success": False, "error": str(e), "table": None, "raw": None}
