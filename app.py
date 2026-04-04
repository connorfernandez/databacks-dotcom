import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. PAGE SETUP
st.set_page_config(page_title="Databacks", page_icon="🐍", layout="wide", initial_sidebar_state="expanded")

# 2. APPLE HEALTH & SAVANT HYBRID CSS
st.markdown("""
<style>
    .stApp { background-color: #F2F2F7; color: #1C1C1E; }
    
    div[data-testid="stDataFrame"] > div {
        background-color: #FFFFFF;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        border: none;
    }
    
    div[data-baseweb="tab-list"] { background-color: #E5E5EA; border-radius: 10px; padding: 4px; gap: 4px; }
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

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("🐍 Databacks")
    page = st.radio("Menu", ["Live Game", "The Lab", "Farm System", "Articles"])
    st.caption("UI Prototype v4.1 - Scorebug Fix")

# 4. MAIN ROUTING LOGIC
if page == "Live Game":
    
    # Savant-style Header
    st.markdown("<h2 style='color: #1C1C1E; font-weight: 400; margin-bottom: 0px;'>Braves vs. Dbacks - 4/3/2026</h2>", unsafe_allow_html=True)
    st.write("") 
    
    tab1, tab2, tab3 = st.tabs(["Live AB", "Scoreboard", "Box Score"])
    
    with tab1:
        st.write("") 
        col1, col2 = st.columns(2)
        
        with col1:
            # Braves Navy Header for Batter (ATL is hitting)
            st.markdown('<div style="background-color: #13274F; color: white; padding: 10px 15px; border-radius: 12px 12px 0 0; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">AT THE PLATE</div>', unsafe_allow_html=True)
            batter_data = pd.DataFrame({
                "Batter": ["Drake Baldwin"], "AB": [2], "H": [0], 
                "Avg EV": ["105.0"], "Hard Hits": [1], "Whiffs": [0], "Whiff %": ["0.0%"]
            })
            st.dataframe(batter_data, hide_index=True, use_container_width=True)
            
            # FOX-STYLE SCOREBUG (Using components.html to prevent glitches)
            components.html("""
            <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: white; border-radius: 16px; padding: 15px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); margin-top: 10px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #E5E5EA;">
                
                <div style="display: flex; gap: 20px; align-items: center;">
                    <div style="text-align: center;">
                        <div style="font-size: 20px; font-weight: 800; color: #1C1C1E;">ATL</div>
                        <div style="font-size: 24px; font-weight: 600; color: #8E8E93;">2</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 20px; font-weight: 800; color: #A71930;">AZ</div>
                        <div style="font-size: 24px; font-weight: 600; color: #8E8E93;">0</div>
                    </div>
                </div>

                <div style="text-align: center; border-left: 1px solid #E5E5EA; border-right: 1px solid #E5E5EA; padding: 0 20px;">
                    <div style="font-size: 16px; font-weight: 700; color: #1C1C1E;">▲ 6th</div>
                    <div style="font-size: 12px; font-weight: 600; color: #8E8E93; margin-top: 4px;">ATL 74.2% WP</div>
                </div>

                <div style="display: flex; gap: 15px; align-items: center;">
                    <div style="text-align: right;">
                        <div style="font-size: 18px; font-weight: 700; color: #1C1C1E;">1 - 1</div>
                        <div style="font-size: 14px; font-weight: 600; color: #8E8E93; margin-top: 2px;">1 Out</div>
                    </div>
                    
                    <div style="position: relative; width: 42px; height: 42px; margin-left: 10px;">
                        <div style="position: absolute; top: 4px; left: 15px; width: 12px; height: 12px; transform: rotate(45deg); border: 2px solid #C7C7CC;"></div>
                        <div style="position: absolute; top: 19px; left: 0px; width: 12px; height: 12px; transform: rotate(45deg); border: 2px solid #C7C7CC;"></div>
                        <div style="position: absolute; top: 19px; left: 30px; width: 12px; height: 12px; transform: rotate(45deg); background-color: #13274F; border: 2px solid #13274F;"></div>
                    </div>
                </div>

            </div>
            """, height=110)

        with col2:
            # Sedona Red Header for Pitcher (Dbacks are pitching)
            st.markdown('<div style="background-color: #A71930; color: white; padding: 10px 15px; border-radius: 12px 12px 0 0; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">ON THE MOUND</div>', unsafe_allow_html=True)
            pitcher_data = pd.DataFrame({
                "Pitcher": ["Eduardo Rodriguez"], "IP": ["5.1"], "K": [4], 
                "Pitches": [72], "Whiffs": [6], "Whiff %": ["18.5%"], "Stuff+": [96] 
            })
            st.dataframe(pitcher_data, hide_index=True, use_container_width=True)
            
            st.write("")
            st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px; margin-top: 10px;">Pitch Sequence</div>', unsafe_allow_html=True)
            
            # PA #37 Pitch Data
            pitch_seq = pd.DataFrame({
                "#": [1, 2, 3],
                "Pitch": ["Sinker", "Curveball", "Cutter"],
                "Result": ["Ball In Dirt", "Called Strike", "In play, out(s)"],
                "Vel": [86.9, 78.3, 86.6],
                "Spin": [2206, 2225, 2203],
                "IVB": [6, -5, 8],
                "HB": [1, 5, 2],
                "Stuff+": [92, 108, 98]
            })

            # Color styling function for pitches
            def color_pitches(val):
                colors = {'Sinker': '#FF8200', 'Curveball': '#00D1ED', 'Cutter': '#933F2C'}
                color = colors.get(val, '#1C1C1E')
                return f'color: {color}; font-weight: 700;'

            styled_seq = pitch_seq.style.map(color_pitches, subset=['Pitch'])

            st.dataframe(
                styled_seq, 
                hide_index=True, 
                use_container_width=True,
                column_config={"#": st.column_config.NumberColumn(width="small")}
            )

    with tab2:
        st.info("Scoreboard components will load here.")
    with tab3:
        st.info("Box score table will load here.")

else:
    st.title(page)
    st.markdown(f"*{page} module is currently under construction. Check back soon.*")
