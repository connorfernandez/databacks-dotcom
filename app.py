import streamlit as st
import pandas as pd

# 1. PAGE SETUP (The Canvas)
st.set_page_config(page_title="Databacks", page_icon="🐍", layout="wide", initial_sidebar_state="expanded")

# 2. APPLE TV / GLASSMORPHISM CSS
st.markdown("""
<style>
    /* Dark Mode Background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Frosted Glass Effect for DataFrames and Metrics */
    div[data-testid="stMetric"], div[data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 10px;
    }
    
    /* Clean Fonts and Sedona Red Accents */
    h1, h2, h3 {
        color: #A71930 !important; 
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    /* Hide the default Streamlit menu for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("🐍 Databacks")
    st.radio("Menu", ["Live GameFeed", "The Lab", "Farm System", "Notebook"])
    st.caption("UI Prototype v1.0")

# 4. MAIN HERO SECTION
st.title("Live GameFeed")
st.caption("AZ Diamondbacks vs. LA Dodgers • Top 4th • 2 Outs")
st.divider()

# 5. SAVANT-STYLE BOX SCORE (Using Dummy Data)
col1, col2 = st.columns(2)

with col1:
    st.subheader("At The Plate")
    # Hitter stats including Hard Hit (HH) and Whiff
    batter_data = pd.DataFrame({
        "Batter": ["Corbin Carroll"],
        "AB": [2],
        "H": [1],
        "Avg EV": ["92.4"],
        "HH": [1],
        "Whiff": [0]
    })
    st.dataframe(batter_data, hide_index=True, use_container_width=True)

with col2:
    st.subheader("On The Mound")
    # Pitcher stats including Whiffs and Stuff+
    pitcher_data = pd.DataFrame({
        "Pitcher": ["Zac Gallen"],
        "IP": ["3.2"],
        "K": [5],
        "Pitches": [54],
        "Whiffs": [8],
        "Stuff+": [112] 
    })
    st.dataframe(pitcher_data, hide_index=True, use_container_width=True)
