import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Databacks", page_icon="🐍", layout="wide", initial_sidebar_state="expanded")

# 2. APPLE HEALTH CSS (Light Mode, Shadows, Rounded Cards)
st.markdown("""
<style>
    /* Light Gray Background like Apple iOS */
    .stApp {
        background-color: #F2F2F7;
        color: #1C1C1E;
    }
    
    /* White Floating Cards with Soft Shadows */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        border: none;
    }
    
    /* Headers - Bold and Clean */
    h1, h2, h3 {
        color: #1C1C1E !important; 
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Custom Glossy Header for Game Title */
    .game-header {
        background: linear-gradient(135deg, #A71930 0%, #8A1528 100%);
        color: white !important;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        box-shadow: 0 10px 20px rgba(167, 25, 48, 0.2);
        margin-bottom: 5px;
    }
    
    /* Hide default Streamlit fluff */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("🐍 Databacks")
    # Updated navigation items
    page = st.radio("Menu", ["Live Game", "The Lab", "Farm System", "Articles"])
    st.caption("UI Prototype v2.0 - Apple Health Edition")

# 4. MAIN ROUTING LOGIC
if page == "Live Game":
    
    # Custom Glossy Header
    st.markdown('<div class="game-header">Dbacks 4 • Dodgers 2</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8E8E93; font-weight: 600;'>Top 4th • 2 Outs • Bases Empty</p>", unsafe_allow_html=True)
    st.write("") # Just a little spacing
    
    # Horizontal Navigation underneath the header
    tab1, tab2, tab3 = st.tabs(["Live AB", "Scoreboard", "Box Score"])
    
    with tab1:
        st.write("") # Spacing
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("At The Plate")
            batter_data = pd.DataFrame({
                "Batter": ["Corbin Carroll"], "AB": [2], "H": [1], 
                "Avg EV": ["92.4"], "HH": [1], "Whiff": [0]
            })
            st.dataframe(batter_data, hide_index=True, use_container_width=True)

        with col2:
            st.subheader("On The Mound")
            pitcher_data = pd.DataFrame({
                "Pitcher": ["Zac Gallen"], "IP": ["3.2"], "K": [5], 
                "Pitches": [54], "Whiffs": [8], "Stuff+": [112] 
            })
            st.dataframe(pitcher_data, hide_index=True, use_container_width=True)
            
    with tab2:
        st.write("") 
        st.subheader("Play-by-Play")
        # Apple Health style notification cards for plays
        st.markdown("""
        <div style="background: white; padding: 15px; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <strong style="color: #A71930; font-size: 18px;">Strikeout Swinging</strong><br>
            <span style="color: #3A3A3C;">Zac Gallen strikes out Shohei Ohtani on a 94mph Four-Seam Fastball.</span>
        </div>
        <div style="background: white; padding: 15px; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <strong style="font-size: 18px;">Groundout</strong><br>
            <span style="color: #3A3A3C;">Mookie Betts grounds out softly to shortstop Geraldo Perdomo.</span>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.write("")
        st.subheader("Team Stats")
        st.info("Traditional box score table will load here.")

# Logic for all the other empty tabs
else:
    st.title(page)
    st.markdown(f"*{page} module is currently under construction. Check back soon.*")
