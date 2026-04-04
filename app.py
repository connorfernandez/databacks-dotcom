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
    div[data-testid="stDataFrame"] > div { background-color: #FFFFFF; border-radius: 0 0 12px 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04); border: none; }
    div[data-baseweb="tab-list"] { background-color: #E5E5EA; border-radius: 10px; padding: 4px; gap: 4px; }
    button[data-baseweb="tab"] { background-color: transparent !important; border-radius: 8px !important; color: #1C1C1E !important; font-weight: 600 !important; padding: 8px 16px !important; border: none !important; }
    button[data-baseweb="tab"][aria-selected="true"] { background-color: #FFFFFF !important; box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important; }
    div[data-baseweb="input"], div[data-baseweb="select"] { border-radius: 8px !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("🐍 Databacks")
    page = st.radio("Menu", ["Live Game", "The Lab", "Farm System", "Articles"])
    st.caption("UI Prototype v14.0 - Live AB Picker")

# 4. MLB STATS-API ENGINE
@st.cache_data(ttl=60) 
def fetch_mlb_game_data(selected_date):
    """Fetches the Game ID and Play-by-Play data for the selected date."""
    date_str = selected_date.strftime("%Y-%m-%d")
    schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}"
    
    try:
        sched_resp = requests.get(schedule_url).json()
        if sched_resp['totalGames'] == 0:
            return None, "No Games Scheduled", []

        games = sched_resp['dates'][0]['games']
        
        # Default to first game, but look for Dbacks
        target_game = games[0]
        for game in games:
            if "Diamondbacks" in game['teams']['away']['team']['name'] or "Diamondbacks" in game['teams']['home']['team']['name']:
                target_game = game
                break
                
        game_pk = target_game['gamePk']
        away_team = target_game['teams']['away']['team']['teamName']
        home_team = target_game['teams']['home']['team']['teamName']
        matchup_text = f"{away_team} @ {home_team}"
        
        # Fetch Play-by-Play
        pbp_url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
        pbp_resp = requests.get(pbp_url).json()
        
        all_plays = pbp_resp.get('liveData', {}).get('plays', {}).get('allPlays', [])
        
        # Filter out empty plays
        valid_plays = [p for p in all_plays if 'matchup' in p and 'result' in p]
        
        return game_pk, matchup_text, valid_plays
        
    except Exception as e:
        return None, "Error Loading API", []

# 5. MAIN ROUTING LOGIC
if page == "Live Game":
    
    # --- DYNAMIC HEADER & CONTROLS ---
    header_col1, header_col2 = st.columns([3, 2])
    
    with header_col2:
        selected_date = st.date_input(
            "Game Date", 
            value=datetime.date(2024, 9, 29), # Defaulting to a known past game for testing
            max_value=datetime.date.today(),
            label_visibility="collapsed"
        )
        
    game_pk, live_header_text, plays = fetch_mlb_game_data(selected_date)
    
    with header_col1:
        st.markdown(f"<h2 style='color: #1C1C1E; font-weight: 400; margin-bottom: 0px;'>{live_header_text}</h2>", unsafe_allow_html=True)

    # --- AT-BAT PICKER ---
    st.write("")
    if plays:
        # Create a formatted list for the dropdown
        play_options = {
            f"{p['about']['halfInning'].upper()} {p['about']['inning']} • {p['matchup']['batter']['fullName']} - {p['result']['event']}": p 
            for p in plays if 'event' in p['result']
        }
        
        selected_play_key = st.selectbox("Select At-Bat", options=list(play_options.keys()), index=len(play_options)-1)
        active_play = play_options[selected_play_key]
        
        # Extract live data from the selected play
        batter_name = active_play['matchup']['batter']['fullName']
        pitcher_name = active_play['matchup']['pitcher']['fullName']
        inning = f"{'▲' if active_play['about']['halfInning'] == 'top' else '▼'} {active_play['about']['inning']}"
        outs = active_play['count']['outs']
        away_score = active_play['result']['awayScore']
        home_score = active_play['result']['homeScore']
        away_abbr = live_header_text.split(" @ ")[0][:3].upper()
        home_abbr = live_header_text.split(" @ ")[1][:3].upper()
        
    else:
        st.warning("No play-by-play data available for this game yet.")
        batter_name, pitcher_name, inning, outs, away_score, home_score, away_abbr, home_abbr = "N/A", "N/A", "-", 0, 0, 0, "AWY", "HME"

    st.write("") 
    tab1, tab2, tab3 = st.tabs(["Live AB", "Scoreboard", "Box Score"])
    
    with tab1:
        st.write("") 
        
        if plays:
            # --- ROW 1: THE SCOREBUG ---
            st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px;">Game Situation</div>', unsafe_allow_html=True)
            components.html(f"""
            <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: white; border-radius: 16px; border: 1px solid #E5E5EA; box-shadow: 0 4px 12px rgba(0,0,0,0.04); display: flex; align-items: stretch; height: 110px; overflow: hidden;">
                
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 0 25px; border-right: 1px solid #E5E5EA; min-width: 360px;">
                    <div style="display: flex; gap: 20px; align-items: center;">
                        <div style="text-align: center;">
                            <div style="font-size: 16px; font-weight: 800; color: #1C1C1E;">{away_abbr}</div>
                            <div style="font-size: 20px; font-weight: 600; color: #8E8E93;">{away_score}</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 16px; font-weight: 800; color: #A71930;">{home_abbr}</div>
                            <div style="font-size: 20px; font-weight: 600; color: #8E8E93;">{home_score}</div>
                        </div>
                    </div>
                    <div style="font-size: 20px; font-weight: 800; color: #1C1C1E;">
                        {inning}
                    </div>
                    <div style="display: flex; justify-content: flex-end; align-items: center; gap: 15px;">
                        <div style="text-align: right;">
                            <div style="font-size: 13px; font-weight: 600; color: #8E8E93; margin-top: 2px;">{outs} Out(s)</div>
                        </div>
                    </div>
                </div>

                <div style="display: flex; flex-direction: column; justify-content: center; gap: 8px; padding: 0 20px; flex-grow: 1;">
                    <div style="background-color: #F9F9F9; padding: 6px 12px; border-radius: 8px; border: 1px solid #E5E5EA; display: flex; justify-content: space-between; align-items: center;">
                        <div><span style="color: #8E8E93; font-size: 12px; font-weight: 700;">AB:</span> <span style="color: #13274F; font-size: 14px; font-weight: 800; margin-left: 4px;">{batter_name}</span></div>
                        <div style="color: #1C1C1E; font-size: 13px; font-weight: 700;"><span style="color: #8E8E93; margin-right: 4px;">wRC+:</span>--</div>
                    </div>
                    <div style="background-color: #F9F9F9; padding: 6px 12px; border-radius: 8px; border: 1px solid #E5E5EA; display: flex; justify-content: space-between; align-items: center;">
                        <div><span style="color: #8E8E93; font-size: 12px; font-weight: 700;">P:</span> <span style="color: #A71930; font-size: 14px; font-weight: 800; margin-left: 4px;">{pitcher_name}</span></div>
                        <div style="color: #1C1C1E; font-size: 13px; font-weight: 700;"><span style="color: #8E8E93; margin-right: 4px;">PC:</span>--</div>
                    </div>
                </div>

                <div style="border-left: 1px solid #E5E5EA; padding: 0 20px; display: flex; flex-direction: column; justify-content: center; min-width: 320px; background-color: #FAFAFA;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div style="font-size: 11px; font-weight: 800; color: #8E8E93; text-transform: uppercase;">Inning Summary</div>
                    </div>
                    <div style="font-size: 13px; font-weight: 600; color: #8E8E93; font-style: italic;">
                        API Inning sequence compiling...
                    </div>
                </div>
            </div>
            """, height=135)

            st.write("")

            # --- ROW 2: THE LIVE AT-BAT (3 Columns) ---
            action_col1, action_col2, action_col3 = st.columns([1.2, 0.8, 1.2])

            with action_col1:
                st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px;">Pitch Usage</div>', unsafe_allow_html=True)
                st.info("API Pitch parsing coming next...")

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
                ax.axis('off')
                st.pyplot(fig, transparent=True)

            with action_col3:
                st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px;">Pitch Sequence</div>', unsafe_allow_html=True)
                st.info("API Pitch sequence coming next...")

            st.write("")

            # --- ROW 3: THE MATCHUP STATS ---
            stat_col1, stat_col2 = st.columns(2)
            
            with stat_col1:
                st.markdown(f"""
                <div style="background-color: #13274F; color: white; padding: 10px 15px; border-radius: 12px 12px 0 0; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">AT THE PLATE</div>
                <div style="background-color: white; border-radius: 0 0 12px 12px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); display: flex; justify-content: space-between; align-items: center;">
                    <div style="text-align: left;">
                        <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">BATTER</div>
                        <div style="font-size: 15px; font-weight: 800; color: #13274F;">{batter_name}</div>
                    </div>
                    <div style="font-size: 13px; font-weight: 600; color: #8E8E93; font-style: italic;">Fetching Season Stats...</div>
                </div>
                """, unsafe_allow_html=True)
                
            with stat_col2:
                st.markdown(f"""
                <div style="background-color: #A71930; color: white; padding: 10px 15px; border-radius: 12px 12px 0 0; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">ON THE MOUND</div>
                <div style="background-color: white; border-radius: 0 0 12px 12px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); display: flex; justify-content: space-between; align-items: center;">
                    <div style="text-align: left;">
                        <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">PITCHER</div>
                        <div style="font-size: 15px; font-weight: 800; color: #A71930;">{pitcher_name}</div>
                    </div>
                    <div style="font-size: 13px; font-weight: 600; color: #8E8E93; font-style: italic;">Fetching Season Stats...</div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.info("Scoreboard components will load here.")
    with tab3:
        st.info("Box score table will load here.")

else:
    st.title(page)
    st.markdown(f"*{page} module is currently under construction. Check back soon.*")
