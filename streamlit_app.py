import streamlit as st
import streamlit.components.v1 as components
import os
from typing import Optional

st.set_page_config(page_title="Transaction Numbers Map", layout="wide")
st.title("From Coast to Coast: Understanding and Predicting BEV Adoption Across Canadian Regions - Supplementary Material")

# --- Config ---
BASE_FOLDER = "transaction_numbers_fsa_map"
DEFAULT_HEIGHT = 700
CACHE_MAX_ENTRIES = 2  # keep cache small to reduce memory use

# --- Data ---
MAPS = [
    {
        "title": "Transactions",
        "file": os.path.join(BASE_FOLDER, "transaction_numbers_map.html"),
        "text": "Map showing the number of transactions by FSA."
    },
    {
        "title": "Transactions per capita",
        "file": os.path.join(BASE_FOLDER, "transaction_numbers_per_capita_map.html"),
        "text": "Map showing the number of transactions per capita by FSA."
    },
    {
        "title": "Proportion of EVs",
        "file": os.path.join(BASE_FOLDER, "ev_proportion_map.html"),
        "text": "Map showing the proportion of electric vehicles by FSA. Figures are in percentages."
    },
    {
        "title": "Zoning 1, Zoning 2 and Original Postal Codes",
        "file": os.path.join(BASE_FOLDER, "canada_zones_toggle.html"),
        "text": "Map the two zoning systems considered, in addition to the base postal codes from which they are derived."
    },
    {
        "title": "Charging Station Accessibility",
        "file": os.path.join(BASE_FOLDER, "charging_station_accessibility.html"),
        "text": "Map showing the accessibility of charging stations across different regions."
    }
]

# --- Helpers ---

def file_mtime(path: str) -> Optional[float]:
    """Return modification time if file exists; else None."""
    try:
        return os.path.getmtime(path)
    except OSError:
        return None

@st.cache_data(show_spinner=False, max_entries=CACHE_MAX_ENTRIES)
def load_map_html(path: str, mtime: Optional[float]) -> str:
    """Read HTML from disk. Cache keyed by (path, mtime) so updates bust cache."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def should_show(i: int) -> bool:
    """Track whether a map has been requested to show."""
    return st.session_state.get(f"show_map_{i}", False)

def mark_show(i: int):
    st.session_state[f"show_map_{i}"] = True

# --- UI Controls (global) ---
st.caption("Tip: only maps you open are loaded into memory. This keeps resource use low.")

# Option to enforce single-map view to minimize concurrent memory use
single_mode = st.toggle("Load only one map at a time (recommended for low-memory hosts)", value=True)

if single_mode:
    # Use a selector so only one map is displayed at a time
    titles = [m["title"] for m in MAPS]
    choice = st.selectbox("Choose a map to open", titles, index=0)
    selected_idx = titles.index(choice)

    m = MAPS[selected_idx]
    with st.container(border=True):
        st.subheader(m["title"])
        st.write(m["text"])

        if not os.path.exists(m["file"]):
            st.error(f"Could not find `{m['file']}`. Make sure it's in the correct folder.")
        else:
            if st.button("Load map", key=f"btn_single_{selected_idx}"):
                mark_show(selected_idx)

            if should_show(selected_idx):
                with st.spinner("Loading map..."):
                    html = load_map_html(m["file"], file_mtime(m["file"]))
                components.html(html, height=DEFAULT_HEIGHT, scrolling=True)
else:
    # Original expander layout, but lazy-load behind a button per map
    for i, m in enumerate(MAPS):
        with st.expander(m["title"], expanded=False):
            st.write(m["text"])
            if not os.path.exists(m["file"]):
                st.error(f"Could not find `{m['file']}`. Make sure it's in the correct folder.")
                continue

            cols = st.columns([1, 1, 6])
            with cols[0]:
                if st.button("Load map", key=f"btn_{i}"):
                    mark_show(i)
            with cols[1]:
                # optional unload to free memory (remove state)
                if st.button("Unload", key=f"unload_{i}"):
                    st.session_state.pop(f"show_map_{i}", None)

            if should_show(i):
                with st.spinner("Loading map..."):
                    html = load_map_html(m["file"], file_mtime(m["file"]))
                components.html(html, height=DEFAULT_HEIGHT, scrolling=True)
