import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Databacks", page_icon="🐍", layout="wide", initial_sidebar_state="expanded")

# 2. APPLE HEALTH & SAVANT HYBRID CSS
st.markdown("""
<style>
    /* Light Gray Background like Apple iOS */
    .stApp {
        background-color: #F2F2F7;
        color: #1C1C1E;
    }
    
    /* Remove default dataframe padding to let our custom headers sit flush */
    div[data-testid="stDataFrame"] > div {
        background-color: #FFFFFF;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        border: none;
    }
    
    /* Apple Style Segmented Control Tabs */
    div[data-baseweb="tab-list"] {
        background-color: #E5E5EA;
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
    }
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 8px !important;
        color: #1C1C1E !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        border: none !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #FFFFFF !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }

    /* Hide default Streamlit fluff */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("🐍 Databacks")
    page = st.radio("Menu", ["Live Game", "The Lab", "Farm System", "Articles"])
    st.caption("UI Prototype v3.0 - Savant Hybrid")

# 4. MAIN ROUTING LOGIC
if page == "Live Game":
    
    # Savant-style Black Header
    st.markdown("<h2 style='color: #1C1C1E; font-weight: 800; margin-bottom: 0px;'>Braves vs. Dbacks - 4/3/2026</h2>", unsafe_allow_html=True)
    st.write("") # Spacing to push tabs down slightly
    
    # Apple Gray Segmented Tabs
    tab1, tab2, tab3 = st.tabs(["Live AB", "Scoreboard", "Box Score"])
    
    with tab1:
        st.write("") # Spacing
        col1, col2 = st.columns(2)
        
        with col1:
            # Sedona Red Header for Dbacks Batter
            st.markdown('<div style="background-color: #A71930; color: white; padding: 10px 15px; border-radius: 12px 12px 0 0; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">AT THE PLATE</div>', unsafe_allow_html=True)
            batter_data = pd.DataFrame({
                "Batter": ["Gabriel Moreno"], 
                "AB": [3], 
                "H": [1], 
                "Avg EV": ["89.4"], 
                "Hard Hits": [2], 
                "Whiffs": [1],
                "Whiff %": ["12.5%"]
            })
            st.dataframe(batter_data, hide_index=True, use_container_width=True)
            
            # The Scorebug (Underneath the Batter)
            st.markdown("""
            <div style="background: white; border-radius: 16px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); margin-top: 20px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 24px; font-weight: 800; color: #1C1C1E; margin-bottom: 5px;">ATL <span style="color: #8E8E93; font-weight: 500; margin-left: 10px;">2</span></div>
                    <div style="font-size: 24px; font-weight: 800; color: #A71930;">AZ <span style="color: #8E8E93; font-weight: 500; margin-left: 17px;">0</span></div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 16px; font-weight: 700; color: #1C1C1E; margin-bottom: 8px;">Top 9th</div>
                    <div style="display: flex; gap: 6px; justify-content: flex-end; margin-bottom: 12px;">
                        <div style="width: 10px; height: 10px; border-radius: 50%; background-color: #A71930;"></div>
                        <div style="width: 10px; height: 10px; border-radius: 50%; background-color: #A71930;"></div>
                        <div style="width: 10px; height: 10px; border-radius: 50%; border: 2px solid #C7C7CC;"></div>
                    </div>
                    <div style="width: 20px; height: 20px; transform: rotate(45deg); border: 2px solid #C7C7CC; float: right; margin-right: 4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Braves Navy Header for Pitcher
            st.markdown('<div style="background-color: #13274F; color: white; padding: 10px 15px; border-radius: 12px 12px 0 0; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">ON THE MOUND</div>', unsafe_allow_html=True)
            pitcher_data = pd.DataFrame({
                "Pitcher": ["Raisel Iglesias"], 
                "IP": ["1.0"], 
                "K": [1], 
                "Pitches": [14], 
                "Whiffs": [3],
                "Whiff %": ["21.4%"],
                "Stuff+": [120] 
            })
            st.dataframe(pitcher_data, hide_index=True, use_container_width=True)
            
            # Live Pitch Sequence Table (Underneath Pitcher)
            st.write("")
            st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px; margin-top: 10px;">Pitch Sequence</div>', unsafe_allow_html=True)
            pitch_seq = pd.DataFrame({
                "#": [1, 2, 3, 4, 5, 6],
                "Pitch": ["Sinker", "4-Seam", "Sinker", "Sinker", "Changeup", "4-Seam"],
                "Result": ["Ball", "Ball", "Called Strike", "Called Strike", "Foul", "In play, out(s)"],
                "Vel": [95.4, 95.1, 94.5, 94.6, 89.9, 95.1],
                "Spin": [2342, 2232, 2185, 2323, 1850, 2326],
                "IVB": [6, 16, 6, 4, 3, 14],
                "HB": [16, 7, 17, 18, 16, 11]
            })
            st.dataframe(pitch_seq, hide_index=True, use_container_width=True)

    # Placeholders for other tabs
    with tab2:
        st.info("Scoreboard components will load here.")
    with tab3:
        st.info("Box score table will load here.")

else:
    st.title(page)
    st.markdown(f"*{page} module is currently under construction. Check back soon.*")
