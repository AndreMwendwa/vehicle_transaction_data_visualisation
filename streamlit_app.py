import streamlit as st
import streamlit.components.v1 as components
import os

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
    }
]

# Loop through and render each map in an expander
for m in maps:
    with st.expander(m["title"], expanded=False):
        st.write(m["text"])
        if not os.path.exists(m["file"]):
            st.error(f"Could not find `{m['file']}`. Make sure it's in the correct folder.")
        else:
            with open(m["file"], "r", encoding="utf-8") as f:
                map_html = f.read()
            components.html(map_html, height=700, scrolling=True)
