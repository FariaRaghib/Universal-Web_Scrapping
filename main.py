import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_html(url):
    """
    Scrape data from an HTML page.
    Tries to detect tables, falls back to div/p text.
    """
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Try extracting a table
        table = soup.find("table")
        if table:
            df = pd.read_html(str(table))[0]
            return {"success": True, "table": df, "raw": None}

        # Fallback: divs
        divs = [d.get_text(strip=True) for d in soup.find_all("div")[:10]]
        if divs:
            return {"success": True, "table": None, "raw": divs}

        # Fallback: paragraphs
        ps = [p.get_text(strip=True) for p in soup.find_all("p")[:10]]
        if ps:
            return {"success": True, "table": None, "raw": ps}

        return {"success": False, "error": "No structured data found"}

    except Exception as e:
        return {"success": False, "error": str(e)}
