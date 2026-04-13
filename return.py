import streamlit as st
import pandas as pd
from datetime import datetime
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Page Configuration
st.set_page_config(page_title="Local File Dashboard", layout="wide")

st.title("📊 Automated Return Dashboard")

# --- 1. SET YOUR GOOGLE SHEET DETAILS HERE ---
SHEET_ID = "1u0jipG6_1k1lO64rwXkFiIVL2Ehoc05Eo9ruZYyvrlI"  # Extract from your Google Sheet URL
GID = "0"  # Tab ID - visible in the URL after &gid=
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

@st.cache_data(ttl=60)  # Refreshes every 60 seconds
def load_local_data(path):
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        return None

df = load_local_data(url)

if df is not None:
    # --- 2. DATA CLEANING ---
    df['Date of closure'] = pd.to_datetime(df['Date of closure'], errors='coerce')
    
    # Handle Godown Column Typo
    godown_col = 'Moved to resspective godown'
    if godown_col not in df.columns:
        found = [c for c in df.columns if 'godown' in str(c).lower()]
        godown_col = found[0] if found else None

    df['Status'] = df['Status'].fillna('Unknown').astype(str).str.strip()
    df[godown_col] = df[godown_col].fillna('No').astype(str).str.strip()

    # --- 3. FILTERING LOGIC ---
    # Show only items NOT moved to godown
    pending_df = df[df[godown_col].str.lower() != 'yes'].copy()

    # Sidebar Filter
    st.sidebar.header("Date Settings")
    use_date_filter = st.sidebar.checkbox("Filter 'Closed' by Date", value=False)
    
    valid_dates = pending_df['Date of closure'].dropna()
    start_def = valid_dates.min().date() if not valid_dates.empty else datetime(2026, 1, 1).date()
    end_def = valid_dates.max().date() if not valid_dates.empty else datetime.now().date()

    selected_range = st.sidebar.date_input("Range (DD/MM/YYYY)", value=(start_def, end_def), format="DD/MM/YYYY")

    # --- 4. METRICS ---
    target_cats = ["Closed", "Re-inspection", "Waiting on Customer", "Unit with Brand", "Pending on Reference ID"]
    cols = st.columns(5)
    
    for i, cat_name in enumerate(target_cats):
        cat_df = pending_df[pending_df['Status'].str.lower() == cat_name.lower()]
        
        if cat_name == "Closed" and use_date_filter:
            if isinstance(selected_range, tuple) and len(selected_range) == 2:
                start, end = selected_range
                cat_df = cat_df[(cat_df['Date of closure'].dt.date >= start) & (cat_df['Date of closure'].dt.date <= end)]
        
        count = len(cat_df)
        with cols[i]:
            st.metric(label=cat_name, value=count)

    # --- 5. DATA TABLE ---
    st.divider()
    st.subheader(f"Detailed View (Total Records: {len(pending_df)})")
    
    display_df = pending_df[['RET', 'Order No', 'Status', 'Date of closure', godown_col]].copy()
    display_df['Date of closure'] = display_df['Date of closure'].dt.strftime('%d/%m/%Y').fillna('No Date')
    
    st.dataframe(display_df, use_container_width=True)
    
    if st.button('🔄 Check for Updates'):
        st.cache_data.clear()
        st.rerun()
