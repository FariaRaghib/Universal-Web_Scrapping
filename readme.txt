# Universal Data Fetcher

Universal Data Fetcher is a web app built with **Streamlit** that helps you fetch data from any website or API without needing to code.  
It supports **HTML scraping** (for sites without APIs) and **API calling** (with or without authentication keys).  
The app also lets you download the extracted data as an **Excel file (.xlsx)** for analysis or reporting.

---

## Features
- **HTML Scraper**: Enter a website URL and automatically extract tables or text.
- **API Caller**: Enter an API endpoint (with optional API key) to fetch structured JSON data.
- **Excel Export**: Save fetched data directly into an Excel file.
- **Error Handling**: Shows warnings and errors for invalid URLs or authentication failures.
- **Professional UI**: Clean layout, search-style input, and centered title for usability.

---

## Example Use Cases
- Collect live **cryptocurrency prices** (CoinGecko API).
- Scrape **COVID-19 stats** tables from Worldometers.
- Fetch **weather data** from OpenWeatherMap with an API key.
- Build quick **datasets for analysis** in Excel, Google Sheets, or Power BI.

---

## Tech Stack
- [Streamlit](https://streamlit.io/) – Frontend & app framework
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) – HTML scraping
- [Requests](https://docs.python-requests.org/en/latest/) – HTTP requests
- [Pandas](https://pandas.pydata.org/) – Data handling & Excel export

---

## Installation & Setup
Clone this repo and install dependencies:

```bash
git clone https://github.com/YOUR-USERNAME/universal-data-fetcher.git
cd universal-data-fetcher
pip install -r requirements.txt
```
