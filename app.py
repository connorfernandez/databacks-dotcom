import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import datetime
import requests

# 1. PAGE SETUP
st.set_page_config(page_title="Databacks", page_icon="🐍", layout="wide", initial_sidebar_state="expanded")

# 2. APPLE HEALTH & SAVANT HYBRID CSS
st.markdown("""
<style>
    .stApp { background-color: #F2F2F7; color: #1C1C1E; }
    
    div[data-testid="stDataFrame"] > div {
        background-color: #FFFFFF; border-radius: 0 0 12px 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04); border: none;
    }
    
    div[data-baseweb="tab-list"] { background-color: #E5E5EA; border-radius: 10px; padding: 4px; gap: 4px; }
    button[data-baseweb="tab"] { background-color: transparent !important; border-radius: 8px !important; color: #1C1C1E !important; font-weight: 600 !important; padding: 8px 16px !important; border: none !important; }
    button[data-baseweb="tab"][aria-selected="true"] { background-color: #FFFFFF !important; box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important; }

    /* Date Picker Styling */
    div[data-baseweb="input"] { border-radius: 8px !important; }
    
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("🐍 Databacks")
    page = st.radio("Menu", ["Live Game", "The Lab", "Farm System", "Articles"])
    st.caption("UI Prototype v13.1 - Dynamic API Header")

# 4. MLB STATS-API ENGINE
@st.cache_data(ttl=30) 
def fetch_mlb_schedule(selected_date):
    """Fetches the real MLB schedule for the selected date."""
    # Format the date perfectly for the MLB URL (e.g., 2026-04-03)
    date_str = selected_date.strftime("%Y-%m-%d")
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}"
    
    try:
        response = requests.get(url).json()
        
        if response['totalGames'] > 0:
            games = response['dates'][0]['games']
            
            # 1. Try to find a Diamondbacks game first
            for game in games:
                away_team = game['teams']['away']['team']['name']
                home_team = game['teams']['home']['team']['name']
                if "Diamondbacks" in away_team or "Diamondbacks" in home_team:
                    return f"{away_team} @ {home_team}"
            
            # 2. If the Dbacks have an off-day, just show the first game of the day
            away_team = games[0]['teams']['away']['team']['name']
            home_team = games[0]['teams']['home']['team']['name']
            return f"{away_team} @ {home_team}"
        else:
            return "No Games Scheduled"
            
    except Exception as e:
        return "Error Loading API"

# 5. MAIN ROUTING LOGIC
if page == "Live Game":
    
    # Date Picker locked between Opening Day 2026 and Today
    header_col1, header_col2 = st.columns([4, 1])
    with header_col2:
        selected_date = st.date_input(
            "Game Date", 
            value=datetime.date(2026, 4, 3), 
            min_value=datetime.date(2026, 3, 26),
            max_value=datetime.date.today(),
            label_visibility="collapsed"
        )
        
    # Ask the API what game happened on this date
    live_header_text = fetch_mlb_schedule(selected_date)
    
    # Inject the real API data into the HTML header
    with header_col1:
        st.markdown(f"<h2 style='color: #1C1C1E; font-weight: 400; margin-bottom: 0px;'>{live_header_text}</h2>", unsafe_allow_html=True)

        
    st.write("") 
    
    tab1, tab2, tab3 = st.tabs(["Live AB", "Scoreboard", "Box Score"])
    
    with tab1:
        st.write("") 
        
        # --- ROW 1: THE SCOREBUG ---
        st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px;">Game Situation</div>', unsafe_allow_html=True)
        components.html("""
        <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: white; border-radius: 16px; border: 1px solid #E5E5EA; box-shadow: 0 4px 12px rgba(0,0,0,0.04); display: flex; align-items: stretch; height: 110px; overflow: hidden;">
            
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 0 25px; border-right: 1px solid #E5E5EA; min-width: 360px;">
                <div style="display: flex; gap: 20px; align-items: center;">
                    <div style="text-align: center;">
                        <div style="font-size: 16px; font-weight: 800; color: #1C1C1E;">ATL</div>
                        <div style="font-size: 20px; font-weight: 600; color: #8E8E93;">2</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 16px; font-weight: 800; color: #A71930;">AZ</div>
                        <div style="font-size: 20px; font-weight: 600; color: #8E8E93;">0</div>
                    </div>
                </div>
                <div style="font-size: 20px; font-weight: 800; color: #1C1C1E;">
                    ▲ 6th
                </div>
                <div style="display: flex; justify-content: flex-end; align-items: center; gap: 15px;">
                    <div style="text-align: right;">
                        <div style="font-size: 18px; font-weight: 800; color: #1C1C1E;">1 - 1</div>
                        <div style="font-size: 13px; font-weight: 600; color: #8E8E93; margin-top: 2px;">1 Out</div>
                    </div>
                    <div style="position: relative; width: 36px; height: 36px;">
                        <div style="position: absolute; top: 4px; left: 13px; width: 10px; height: 10px; transform: rotate(45deg); border: 2px solid #C7C7CC;"></div>
                        <div style="position: absolute; top: 16px; left: 0px; width: 10px; height: 10px; transform: rotate(45deg); border: 2px solid #C7C7CC;"></div>
                        <div style="position: absolute; top: 16px; left: 26px; width: 10px; height: 10px; transform: rotate(45deg); background-color: #13274F; border: 2px solid #13274F;"></div>
                    </div>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; justify-content: center; gap: 8px; padding: 0 20px; flex-grow: 1;">
                <div style="background-color: #F9F9F9; padding: 6px 12px; border-radius: 8px; border: 1px solid #E5E5EA; display: flex; justify-content: space-between; align-items: center;">
                    <div><span style="color: #8E8E93; font-size: 12px; font-weight: 700;">AB:</span> <span style="color: #13274F; font-size: 14px; font-weight: 800; margin-left: 4px;">Drake Baldwin</span></div>
                    <div style="color: #1C1C1E; font-size: 13px; font-weight: 700;"><span style="color: #8E8E93; margin-right: 4px;">wRC+:</span>112</div>
                </div>
                <div style="background-color: #F9F9F9; padding: 6px 12px; border-radius: 8px; border: 1px solid #E5E5EA; display: flex; justify-content: space-between; align-items: center;">
                    <div><span style="color: #8E8E93; font-size: 12px; font-weight: 700;">P:</span> <span style="color: #A71930; font-size: 14px; font-weight: 800; margin-left: 4px;">Eduardo Rodriguez</span></div>
                    <div style="color: #1C1C1E; font-size: 13px; font-weight: 700;"><span style="color: #8E8E93; margin-right: 4px;">PC:</span>72</div>
                </div>
            </div>

            <div style="border-left: 1px solid #E5E5EA; padding: 0 20px; display: flex; flex-direction: column; justify-content: center; min-width: 320px; background-color: #FAFAFA;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="font-size: 11px; font-weight: 800; color: #8E8E93; text-transform: uppercase;">Inning Summary</div>
                    <div style="display: flex; gap: 15px; text-align: right;">
                        <div style="font-size: 11px; font-weight: 700; color: #8E8E93; width: 35px;">EV</div>
                        <div style="font-size: 11px; font-weight: 700; color: #8E8E93; width: 35px;">xBA</div>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <div style="font-size: 13px; font-weight: 800; color: #13274F; flex-grow: 1;">
                        <span style="color: #8E8E93; font-weight: 700; margin-right: 6px;">1</span>Harris II <span style="font-size: 11px; font-weight: 600; color: #1C1C1E; margin-left: 6px;">Single</span>
                    </div>
                    <div style="display: flex; gap: 15px; text-align: right;">
                        <div style="font-size: 12px; font-weight: 700; color: #1C1C1E; width: 35px;">105.4</div>
                        <div style="font-size: 12px; font-weight: 700; color: #8E8E93; width: 35px;">.780</div>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 13px; font-weight: 800; color: #13274F; flex-grow: 1;">
                        <span style="color: #8E8E93; font-weight: 700; margin-right: 6px;">2</span>Riley <span style="font-size: 11px; font-weight: 600; color: #1C1C1E; margin-left: 6px;">Flyout</span>
                    </div>
                    <div style="display: flex; gap: 15px; text-align: right;">
                        <div style="font-size: 12px; font-weight: 700; color: #1C1C1E; width: 35px;">88.2</div>
                        <div style="font-size: 12px; font-weight: 700; color: #8E8E93; width: 35px;">.040</div>
                    </div>
                </div>
            </div>

        </div>
        """, height=135)

        st.write("")

        # --- ROW 2: THE LIVE AT-BAT (3 Columns) ---
        action_col1, action_col2, action_col3 = st.columns([1.2, 0.8, 1.2])

        # LEFT: PITCH USAGE
        with action_col1:
            st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px;">Pitch Usage</div>', unsafe_allow_html=True)
            st.markdown("""
            <div style="background-color: white; border-radius: 12px; padding: 15px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); border: 1px solid #E5E5EA;">
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; text-align: center; border-bottom: 1px solid #E5E5EA; padding-bottom: 8px; margin-bottom: 8px;">
                    <div style="font-size: 11px; font-weight: 700; color: #8E8E93; text-align: left;">PITCH</div>
                    <div style="font-size: 11px; font-weight: 700; color: #8E8E93;">GAME</div>
                    <div style="font-size: 11px; font-weight: 700; color: #8E8E93;">SEASON</div>
                    <div style="font-size: 11px; font-weight: 700; color: #8E8E93;">VELO</div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; text-align: center; align-items: center; padding: 6px 0;">
                    <div style="font-size: 14px; font-weight: 800; color: #FF8200; text-align: left;">SI</div>
                    <div style="font-size: 14px; font-weight: 800; color: #1C1C1E;">44%</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93;">41%</div>
                    <div style="font-size: 13px; font-weight: 700; color: #1C1C1E;">86.7</div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; text-align: center; align-items: center; padding: 6px 0;">
                    <div style="font-size: 14px; font-weight: 800; color: #933F2C; text-align: left;">FC</div>
                    <div style="font-size: 14px; font-weight: 800; color: #1C1C1E;">26%</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93;">22%</div>
                    <div style="font-size: 13px; font-weight: 700; color: #1C1C1E;">85.9</div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; text-align: center; align-items: center; padding: 6px 0;">
                    <div style="font-size: 14px; font-weight: 800; color: #00D1ED; text-align: left;">CU</div>
                    <div style="font-size: 14px; font-weight: 800; color: #1C1C1E;">18%</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93;">15%</div>
                    <div style="font-size: 13px; font-weight: 700; color: #1C1C1E;">77.8</div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; text-align: center; align-items: center; padding: 6px 0;">
                    <div style="font-size: 14px; font-weight: 800; color: #D22D49; text-align: left;">FF</div>
                    <div style="font-size: 14px; font-weight: 800; color: #1C1C1E;">12%</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93;">22%</div>
                    <div style="font-size: 13px; font-weight: 700; color: #1C1C1E;">88.1</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # CENTER: 2D STRIKE ZONE
        with action_col2:
            st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px; text-align: center;">Pitch Location</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(3, 3))
            fig.patch.set_facecolor('#F2F2F7') 
            ax.set_facecolor('#F2F2F7')
            ax.set_xlim(-2, 2)
            ax.set_ylim(0, 5)

            plate = patches.Polygon([(-0.71, 0.1), (0.71, 0.1), (0.71, 0.3), (0, 0.5), (-0.71, 0.3)], closed=True, facecolor='#E5E5EA', edgecolor='#C7C7CC')
            ax.add_patch(plate)

            zone = patches.Rectangle((-0.71, 1.5), 1.42, 2.0, linewidth=2, edgecolor='#8E8E93', facecolor='none', linestyle='-')
            ax.add_patch(zone)

            ax.scatter(0.3, 0.8, color='#FF8200', s=200, zorder=5, edgecolor='white', linewidth=1.5)
            ax.text(0.3, 0.8, '1', color='white', fontsize=9, ha='center', va='center', weight='bold', zorder=6)
            
            ax.scatter(-0.5, 1.8, color='#00D1ED', s=200, zorder=5, edgecolor='white', linewidth=1.5)
            ax.text(-0.5, 1.8, '2', color='white', fontsize=9, ha='center', va='center', weight='bold', zorder=6)

            ax.scatter(0.1, 2.6, color='#933F2C', s=200, zorder=5, edgecolor='white', linewidth=1.5)
            ax.text(0.1, 2.6, '3', color='white', fontsize=9, ha='center', va='center', weight='bold', zorder=6)

            ax.axis('off')
            st.pyplot(fig, transparent=True)

        # RIGHT: PITCH SEQUENCE 
        with action_col3:
            st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px;">Pitch Sequence</div>', unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: white; border-radius: 12px; padding: 15px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); border: 1px solid #E5E5EA;">
                <div style="display: grid; grid-template-columns: 0.5fr 1fr 2fr 1fr 1fr; text-align: center; border-bottom: 1px solid #E5E5EA; padding-bottom: 8px; margin-bottom: 8px;">
                    <div style="font-size: 11px; font-weight: 700; color: #8E8E93; text-align: left;">#</div>
                    <div style="font-size: 11px; font-weight: 700; color: #8E8E93; text-align: left;">PITCH</div>
                    <div style="font-size: 11px; font-weight: 700; color: #8E8E93; text-align: left;">RESULT</div>
                    <div style="font-size: 11px; font-weight: 700; color: #8E8E93;">VELO</div>
                    <div style="font-size: 11px; font-weight: 700; color: #8E8E93;">STUFF+</div>
                </div>
                <div style="display: grid; grid-template-columns: 0.5fr 1fr 2fr 1fr 1fr; text-align: center; align-items: center; padding: 6px 0;">
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; text-align: left;">1</div>
                    <div style="font-size: 14px; font-weight: 800; color: #FF8200; text-align: left;">SI</div>
                    <div style="font-size: 13px; font-weight: 600; color: #1C1C1E; text-align: left;">Ball In Dirt</div>
                    <div style="font-size: 13px; font-weight: 700; color: #1C1C1E;">86.9</div>
                    <div><span style="font-size: 12px; font-weight: 800; color: #1C1C1E; background-color: #B4C6E7; border-radius: 4px; padding: 2px 6px;">92</span></div>
                </div>
                <div style="display: grid; grid-template-columns: 0.5fr 1fr 2fr 1fr 1fr; text-align: center; align-items: center; padding: 6px 0;">
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; text-align: left;">2</div>
                    <div style="font-size: 14px; font-weight: 800; color: #00D1ED; text-align: left;">CU</div>
                    <div style="font-size: 13px; font-weight: 600; color: #1C1C1E; text-align: left;">Called Strike</div>
                    <div style="font-size: 13px; font-weight: 700; color: #1C1C1E;">78.3</div>
                    <div><span style="font-size: 12px; font-weight: 800; color: #1C1C1E; background-color: #F1A7AA; border-radius: 4px; padding: 2px 6px;">108</span></div>
                </div>
                <div style="display: grid; grid-template-columns: 0.5fr 1fr 2fr 1fr 1fr; text-align: center; align-items: center; padding: 6px 0;">
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; text-align: left;">3</div>
                    <div style="font-size: 14px; font-weight: 800; color: #933F2C; text-align: left;">FC</div>
                    <div style="font-size: 13px; font-weight: 600; color: #1C1C1E; text-align: left;">In play, out(s)</div>
                    <div style="font-size: 13px; font-weight: 700; color: #1C1C1E;">86.6</div>
                    <div><span style="font-size: 12px; font-weight: 800; color: #1C1C1E; background-color: #E5E5EA; border-radius: 4px; padding: 2px 6px;">98</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.write("")

        # --- ROW 3: THE MATCHUP STATS (2 Columns) ---
        stat_col1, stat_col2 = st.columns(2)
        
        with stat_col1:
            st.markdown("""
            <div style="background-color: #13274F; color: white; padding: 10px 15px; border-radius: 12px 12px 0 0; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">AT THE PLATE</div>
            <div style="background-color: white; border-radius: 0 0 12px 12px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); display: grid; grid-template-columns: 2.2fr 0.8fr 0.8fr 0.8fr 0.8fr 1.2fr 1fr; text-align: center; align-items: center;">
                <div style="text-align: left;">
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">BATTER</div>
                    <div style="font-size: 15px; font-weight: 800; color: #13274F;">Drake Baldwin</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-top: 4px;">Season</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">AB</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">2</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-top: 4px;">.284</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">H</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">0</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-top: 4px;">61</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">BB</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">1</div>
                    <div style="font-size: 13px; font-weight: 800; color: #1C1C1E; background-color: #E5E5EA; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">11.2%</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">K</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">1</div>
                    <div style="font-size: 13px; font-weight: 800; color: #1C1C1E; background-color: #F1A7AA; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">16.5%</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">AVG EV</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">105.0</div>
                    <div style="font-size: 13px; font-weight: 800; color: white; background-color: #D22D49; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">91.2</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">WHIFFS</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">0</div>
                    <div style="font-size: 13px; font-weight: 800; color: white; background-color: #D22D49; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">14.5%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with stat_col2:
            st.markdown("""
            <div style="background-color: #A71930; color: white; padding: 10px 15px; border-radius: 12px 12px 0 0; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">ON THE MOUND</div>
            <div style="background-color: white; border-radius: 0 0 12px 12px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); display: grid; grid-template-columns: 2.2fr 1fr 1fr 1fr 1.2fr 1fr; text-align: center; align-items: center;">
                <div style="text-align: left;">
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">PITCHER</div>
                    <div style="font-size: 15px; font-weight: 800; color: #A71930;">Eduardo Rodriguez</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-top: 4px;">Season</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">IP</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">5.1</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-top: 4px;">114.0</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">K</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">4</div>
                    <div style="font-size: 13px; font-weight: 800; color: #1C1C1E; background-color: #F1A7AA; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">24.5%</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">BB</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">2</div>
                    <div style="font-size: 13px; font-weight: 800; color: #1C1C1E; background-color: #E5E5EA; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">7.8%</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">WHIFFS</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">6</div>
                    <div style="font-size: 13px; font-weight: 800; color: #1C1C1E; background-color: #F1A7AA; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">28.5%</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">STUFF+</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">96</div>
                    <div style="font-size: 13px; font-weight: 800; color: #1C1C1E; background-color: #E5E5EA; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">98</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.info("Scoreboard components will load here.")
    with tab3:
        st.info("Box score table will load here.")

else:
    st.title(page)
    st.markdown(f"*{page} module is currently under construction. Check back soon.*")
