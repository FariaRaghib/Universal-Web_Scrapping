import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_html(url: str):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # --- Try Worldometers-specific table ---
        target_table = soup.find("table", {"id": "main_table_countries_today"})
        if target_table:
            headers = [th.get_text(strip=True) for th in target_table.find_all("th")]
            rows = []
            for tr in target_table.find_all("tr"):
                cols = [td.get_text(strip=True) for td in tr.find_all("td")]
                if cols:
                    rows.append(cols)

            if headers and rows:
                df = pd.DataFrame(rows, columns=headers[:len(rows[0])])
                return {"success": True, "table": df, "raw": None, "error": None}

        # --- Fallback: generic tables ---
        try:
            tables = pd.read_html(response.text)
            if tables:
                return {"success": True, "table": tables[0], "raw": None, "error": None}
        except Exception:
            pass  # ignore parsing errors

        # --- If no tables, return raw text ---
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        if paragraphs:
            return {"success": True, "table": None, "raw": "\n".join(paragraphs), "error": None}

        return {"success": False, "error": "No tables or readable text found", "table": None, "raw": None}

    except Exception as e:
        return {"success": False, "error": str(e), "table": None, "raw": None}


