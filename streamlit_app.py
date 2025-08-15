import streamlit as st
import streamlit.components.v1 as components
import os
from Utils.utils import get_years, make_html_table_from_dataframe, replace_semicolon_with_linebreak, get_all_column_values
import pandas as pd

# ---- Lazy-load helpers ----
@st.cache_data(show_spinner=False)
def _read_html_once(path, mtime):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@st.cache_data(show_spinner=False)
def _load_incentives_html_once(xlsx_path, sheet_name, mtime):
    df = pd.read_excel(xlsx_path, sheet_name=sheet_name)
    # keep your existing HTML builder (now with link columns)
    return make_html_table_from_dataframe(df, link_columns=["Eligible vehicles", "Source"])

def maps():
    st.set_page_config(page_title="Transaction Numbers Map", layout="wide")
    st.title("From Coast to Coast: Understanding and Predicting BEV Adoption Across Canadian Regions - Supplementary Material")

    # Base folder where your maps live
    base_folder = "transaction_numbers_fsa_map"

    # Define your HTML files and titles
    maps = [
        {
            "title": "Transactions",
            "file": os.path.join(base_folder, "transaction_numbers_map.html"),
            "text": "Map showing the number of transactions by FSA."
        },
        {
            "title": "Transactions per capita",
            "file": os.path.join(base_folder, "transaction_numbers_per_capita_map.html"),
            "text": "Map showing the number of transactions per capita by FSA."
        },
        {
            "title": "Proportion of EVs",
            "file": os.path.join(base_folder, "ev_proportion_map.html"),
            "text": "Map showing the proportion of electric vehicles by FSA. Figures are in percentages."
        },
        {
            "title": "Zoning 1, Zoning 2 and Original Postal Codes",
            "file": os.path.join(base_folder, "canada_zones_toggle.html"),
            "text": "Map the two zoning systems considered, in addition to the base postal codes from which they are derived."
        },
        {
            "title": "Charging Station Accessibility",
            "file": os.path.join(base_folder, "charging_station_accessibility.html"),
            "text": "Map showing the accessibility of charging stations across different regions."
        }
    ]

    # Loop through and render each map in an expander
    for m in maps:
        with st.expander(m["title"], expanded=False):
            st.write(m["text"])
            if not os.path.exists(m["file"]):
                st.error(f"Could not find `{m['file']}`. Make sure it's in the correct folder.")
            else:
                # Lazy-load only when the expander is opened; cache thereafter
                mtime = os.path.getmtime(m["file"])
                map_html = _read_html_once(m["file"], mtime)
                components.html(map_html, height=700, scrolling=True)

def tables():
    st.title("EV Adoption Incentives")
    st.write("Data on EV adoption incentives across different provinces.")
    with st.expander("Summary of Incentives Data", expanded=False):
        # Load the incentives data only when opened; cache thereafter
        xlsx_path = "EV_incentives_sum_edited.xlsx"
        sheet = "EV_incentives_sum"
        if not os.path.exists(xlsx_path):
            st.error(f"Could not find `{xlsx_path}`. Make sure it's in the correct folder.")
        else:
            mtime = os.path.getmtime(xlsx_path)
            incentives_data_html = _load_incentives_html_once(xlsx_path, sheet, mtime)
            # Display the HTML table
            st.markdown(incentives_data_html, unsafe_allow_html=True)

if __name__ == "__main__":
    tables()
    maps()
