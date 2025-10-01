import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_html(url: str):
    try:
        # Step 1: Fetch page (with headers to avoid blocking)
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Step 2: Find all tables
        tables = soup.find_all("table")
        if not tables:
            return {"success": False, "error": "No tables found", "table": None, "raw": None}

        all_dfs = []

        for table in tables:
            # Extract headers (from thead or first row)
            headers = []
            header_row = table.find("thead")
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all("th")]
            else:
                first_row = table.find("tr")
                if first_row:
                    headers = [th.get_text(strip=True) for th in first_row.find_all(["th", "td"])]

            # Extract all rows
            rows = []
            for tr in table.find_all("tr"):
                cols = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                if cols:
                    rows.append(cols)

            # Step 3: Create DataFrame safely
            if headers and rows:
                # Pad/truncate headers to match row length
                max_len = max(len(r) for r in rows)
                headers = headers[:max_len] + [f"Column {i}" for i in range(len(headers), max_len)]
                df = pd.DataFrame(rows[1:], columns=headers)  # skip header row
            else:
                df = pd.DataFrame(rows)

            if not df.empty:
                all_dfs.append(df)

        if all_dfs:
            return {"success": True, "table": all_dfs[0], "raw": None, "error": None}
        else:
            return {"success": False, "error": "Tables found but empty after parsing", "table": None, "raw": None}

    except Exception as e:
        return {"success": False, "error": str(e), "table": None, "raw": None}
