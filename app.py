import streamlit as st
import pandas as pd
from io import BytesIO
from api import fetch_api
from main import scrape_html

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="Universal Data Fetcher",
    layout="wide",
)

# ------------------------------
# Custom CSS for Styling
# ------------------------------
st.markdown("""
    <style>
    /* Background */
    .main {
        background-color: #f8f9fb;
        padding: 2rem;
    }

    /* Center Title */
    .title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 1rem;
    }

    /* Search Bar */
    .stTextInput>div>div>input {
        border: 2px solid #4a6cf7;
        border-radius: 10px;
        padding: 0.6em;
        font-size: 1rem;
    }

    /* Buttons */
    .stButton button {
        background: #4a6cf7;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        border: none;
        transition: 0.3s;
    }
    .stButton button:hover {
        background: #354fcf;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# Sidebar Navigation
# ------------------------------
st.sidebar.title("Navigation")
nav = st.sidebar.radio("Go to:", ["Home", "Docs", "Examples", "Contact"])

# ------------------------------
# Title
# ------------------------------
st.markdown("<h1 class='title'>Universal Data Fetcher</h1>", unsafe_allow_html=True)

if nav == "Home":
    # ------------------------------
    # About Section
    # ------------------------------
    with st.expander("About this Website", expanded=True):
        st.markdown("""
        **Universal Data Fetcher** helps you collect data from websites or APIs.

        **How it works:**
        - **HTML Scraper** → Enter a website URL, and the app will try to extract tables or text.  
        - **API Caller** → Enter an API endpoint (with API key if required).  

        **Use Cases:**  
        - Crypto/stock prices  
        - Product data  
        - API testing  
        - Dataset building
        """)

    # ------------------------------
    # User Inputs
    # ------------------------------
    st.markdown("### Choose Your Mode")

    col1, col2 = st.columns([2, 1])

    with col1:
        mode = st.radio("Select Data Fetch Mode:", ["HTML Scraper", "API Caller"], horizontal=True)
        url = st.text_input("Enter Website URL or API Endpoint:")

    with col2:
        api_key = None
        if mode == "API Caller":
            need_auth = st.checkbox("API requires authentication?")
            if need_auth:
                api_key = st.text_input("Enter your API Key:", type="password")

    # ------------------------------
    # Fetch Data
    # ------------------------------
    st.markdown("---")
    fetch = st.button("Fetch Data Now")

    def to_excel(df):
        """Convert DataFrame to Excel in memory."""
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Data")
        return output.getvalue()

    if fetch:
        if not url:
            st.warning("Please enter a valid URL or API endpoint.")
        else:
            if mode == "HTML Scraper":
                result = scrape_html(url)
                if result["success"]:
                    if result["table"] is not None:
                        st.success("Table detected from HTML")
                        st.dataframe(result["table"], use_container_width=True)

                        # Download option
                        excel_data = to_excel(result["table"])
                        st.download_button(
                            label="Download Excel File",
                            data=excel_data,
                            file_name="scraped_data.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                    elif result["raw"] is not None:
                        st.info("No table found. Showing raw text:")
                        st.write(result["raw"])
                else:
                    st.error(f"Error: {result['error']}")

            elif mode == "API Caller":
                result = fetch_api(url, api_key)
                if result["success"]:
                    st.success("API response received")
                    st.json(result["json"])

                    if result["table"] is not None:
                        st.write("Converted to table:")
                        st.dataframe(result["table"], use_container_width=True)

                        # Download option
                        excel_data = to_excel(result["table"])
                        st.download_button(
                            label="Download Excel File",
                            data=excel_data,
                            file_name="api_data.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                else:
                    st.error(f"Error: {result['error']}")

elif nav == "Docs":
    st.header("Documentation")
    st.markdown(
        """
        <style>
        .doc-section h3 {
            color: #2a9d8f; 
            margin-top: 20px;
        }
        .doc-section ul {
            margin-left: 20px;
            line-height: 1.6;
        }
        .doc-section code {
            background: #f1f1f1;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 90%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="doc-section">

        ### 1. Modes of Data Fetching
        - <b>HTML Scraper</b>  
          - Enter a <code>website URL</code> (example: <code>https://example.com/prices</code>)  
          - The app will attempt to extract <b>tables</b> or <b>text content</b>.  
          - Useful when a website doesn’t provide an API.  

        - <b>API Caller</b>  
          - Enter a valid <code>API endpoint</code> (example: <code>https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd</code>)  
          - If authentication is needed, enable the checkbox and provide your <b>API key</b>.  
          - Data is automatically structured into a table if possible.  

        ---

        ### 2. Downloading Data
        - After fetching, you can <b>download results</b> as an <code>.xlsx</code> file.  
        - Works with <b>Excel</b>, <b>Google Sheets</b>, or <b>Power BI</b>.  

        ---

        ### 3. Error Handling
        - Invalid URL → shows a warning  
        - Scraping fails → raw error is displayed  
        - Wrong API key/endpoint → error message  

        ---

        ### 4. Limitations
        - Some websites <b>block scraping</b> or need JavaScript (not supported yet).  
        - API endpoints must return <b>valid JSON</b>.  

        </div>
        """,
        unsafe_allow_html=True
    )
elif nav == "Examples":
    st.header("Examples")
    st.markdown(
        """
        <style>
        .example-section h3 {
            color: #264653; 
            margin-top: 25px;
        }
        .example-section code {
            background: #f4f4f4;
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 90%;
        }
        .example-card {
            background: #f9f9f9;
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.08);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="example-section">

        <div class="example-card">
        <h3>Example 1: HTML Scraper</h3>
        <b>URL:</b> <code>https://www.worldometers.info/coronavirus/</code><br>
        <b>Result:</b> Extracts live COVID-19 statistics tables.<br>
        <b>Use Case:</b> Data analysis, dashboards, or academic reports.
        </div>

        <div class="example-card">
        <h3>Example 2: Public API (No Key Required)</h3>
        <b>Endpoint:</b><br>
        <code>https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd</code><br>
        <b>Result:</b> Live cryptocurrency prices (Bitcoin, Ethereum, etc.).<br>
        <b>Use Case:</b> Financial analysis, price trackers, trading bots.
        </div>

        <div class="example-card">
        <h3>Example 3: Authenticated API</h3>
        <b>Endpoint:</b> A weather API like OpenWeatherMap:<br>
        <code>https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY</code><br>
        <b>Result:</b> Current weather data for London.<br>
        <b>Use Case:</b> Weather dashboards, IoT projects.
        </div>

        <hr>
        <p><i>👉 Try these URLs in the input bar to see how it works!</i></p>

        </div>
        """,
        unsafe_allow_html=True
    )
elif nav == "Contact":
    st.header("Contact")
    st.markdown(
        """
        <style>
        .contact-section h3 {
            color: #264653;
            margin-top: 25px;
        }
        .contact-card {
            background: #f9f9f9;
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.08);
        }
        .contact-card a {
            text-decoration: none;
            color: #2a9d8f;
            font-weight: 600;
        }
        .contact-card a:hover {
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="contact-section">

        <div class="contact-card">
        <h3>Email</h3>
        <p>General Support: <b>nestpythonic@gmail.com</b></p>
        </div>

        <div class="contact-card">
        <h3>Social Media</h3>
        <p><a href="https://github.com/FariaRaghib" target="_blank">GitHub</a></p>
        <p><a href="https://www.linkedin.com/in/fariaraghib" target="_blank">LinkedIn</a></p>
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------------
# Footer
# ------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>© 2025 Universal Data Fetcher</p>",
    unsafe_allow_html=True,
)
