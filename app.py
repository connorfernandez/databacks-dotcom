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
    st.caption("UI Prototype v15.0 - Live 2026 Engine")

# 4. MLB STATS-API ENGINE
@st.cache_data(ttl=60) 
def fetch_mlb_game_data(selected_date):
    """Fetches the Game ID and Play-by-Play data for the selected date."""
    date_str = selected_date.strftime("%Y-%m-%d")
    schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}"
    
    try:
        sched_resp = requests.get(schedule_url).json()
        if sched_resp.get('totalGames', 0) == 0:
            return None, "No Games Scheduled", []

        games = sched_resp['dates'][0]['games']
        
        target_game = games[0]
        for game in games:
            away_name = game.get('teams', {}).get('away', {}).get('team', {}).get('name', '')
            home_name = game.get('teams', {}).get('home', {}).get('team', {}).get('name', '')
            if "Diamondbacks" in away_name or "Diamondbacks" in home_name:
                target_game = game
                break
                
        game_pk = target_game.get('gamePk')
        
        away_team = target_game.get('teams', {}).get('away', {}).get('team', {}).get('name', 'Away')
        home_team = target_game.get('teams', {}).get('home', {}).get('team', {}).get('name', 'Home')
        matchup_text = f"{away_team} @ {home_team}"
        
        pbp_url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
        pbp_resp = requests.get(pbp_url).json()
        
        all_plays = pbp_resp.get('liveData', {}).get('plays', {}).get('allPlays', [])
        valid_plays = [p for p in all_plays if 'matchup' in p and 'result' in p]
        
        return game_pk, matchup_text, valid_plays
        
    except Exception as e:
        return None, "Error Loading API", []

# 5. MAIN ROUTING LOGIC
if page == "Live Game":
    
    header_col1, header_col2 = st.columns([3, 2])
    
    with header_col2:
        # Strictly locked to the 2026 season
        selected_date = st.date_input(
            "Game Date", 
            value=datetime.date(2026, 4, 3), 
            min_value=datetime.date(2026, 3, 26), 
            max_value=datetime.date.today(),
            label_visibility="collapsed"
        )
        
    game_pk, live_header_text, plays = fetch_mlb_game_data(selected_date)
    
    with header_col1:
        st.markdown(f"<h2 style='color: #1C1C1E; font-weight: 400; margin-bottom: 0px;'>{live_header_text}</h2>", unsafe_allow_html=True)

    st.write("")
    if plays:
        play_options = {
            f"{p['about']['halfInning'].upper()} {p['about']['inning']} • {p['matchup']['batter']['fullName']} - {p['result']['event']}": p 
            for p in plays if 'event' in p['result']
        }
        
        selected_play_key = st.selectbox("Select At-Bat", options=list(play_options.keys()), index=len(play_options)-1)
        active_play = play_options[selected_play_key]
        
        # --- PARSE MATCHUP DATA ---
        batter_name = active_play['matchup']['batter']['fullName']
        pitcher_name = active_play['matchup']['pitcher']['fullName']
        inning = f"{'▲' if active_play['about']['halfInning'] == 'top' else '▼'} {active_play['about']['inning']}"
        outs = active_play['count']['outs']
        away_score = active_play['result']['awayScore']
        home_score = active_play['result']['homeScore']
        
        if " @ " in live_header_text:
            away_abbr = live_header_text.split(" @ ")[0].split(" ")[-1][:3].upper()
            home_abbr = live_header_text.split(" @ ")[1].split(" ")[-1][:3].upper()
        else:
            away_abbr, home_abbr = "AWY", "HME"

        # --- PARSE INNING SUMMARY ---
        current_inning_num = active_play['about']['inning']
        current_half = active_play['about']['halfInning']
        current_atBatIndex = active_play['about']['atBatIndex']
        
        inning_plays = [p for p in plays if p['about']['inning'] == current_inning_num and p['about']['halfInning'] == current_half and p['about']['atBatIndex'] <= current_atBatIndex]
        
        inning_summary_html = ""
        for i, p in enumerate(inning_plays):
            b_name = p['matchup']['batter']['fullName'].split(' ')[-1] # Last name
            result_event = p['result'].get('event', 'In Progress')
            
            inning_summary_html += f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                <div style="font-size: 13px; font-weight: 800; color: #13274F; flex-grow: 1;">
                    <span style="color: #8E8E93; font-weight: 700; margin-right: 6px;">{i+1}</span>{b_name} <span style="font-size: 11px; font-weight: 600; color: #1C1C1E; margin-left: 6px;">{result_event}</span>
                </div>
                <div style="display: flex; gap: 15px; text-align: right;">
                    <div style="font-size: 12px; font-weight: 700; color: #1C1C1E; width: 35px;">--</div>
                    <div style="font-size: 12px; font-weight: 700; color: #8E8E93; width: 35px;">--</div>
                </div>
            </div>
            """

        # --- PARSE PITCH SEQUENCE ---
        pitch_events = [e for e in active_play.get('playEvents', []) if e.get('isPitch')]
        pitch_sequence_html = ""
        plot_pitches = []
        
        pitch_colors = {'FF': '#D22D49', 'SI': '#FF8200', 'FC': '#933F2C', 'CU': '#00D1ED', 'SL': '#E3E1A6', 'CH': '#1DBE3A', 'FS': '#1DBE3A', 'ST': '#E3E1A6', 'SV': '#E3E1A6'}
        
        for i, pitch in enumerate(pitch_events):
            p_code = pitch.get('details', {}).get('type', {}).get('code', 'UN')
            p_result = pitch.get('details', {}).get('description', 'Unknown')
            p_velo = pitch.get('pitchData', {}).get('startSpeed', '-')
            
            # Extract coordinates for the 2D plot
            pX = pitch.get('pitchData', {}).get('coordinates', {}).get('pX')
            pZ = pitch.get('pitchData', {}).get('coordinates', {}).get('pZ')
            p_color = pitch_colors.get(p_code, '#1C1C1E')
            
            if pX is not None and pZ is not None:
                plot_pitches.append({'x': pX, 'z': pZ, 'color': p_color, 'num': i+1})
                
            pitch_sequence_html += f"""
            <div style="display: grid; grid-template-columns: 0.5fr 1fr 2fr 1fr 1fr; text-align: center; align-items: center; padding: 6px 0;">
                <div style="font-size: 13px; font-weight: 700; color: #8E8E93; text-align: left;">{i+1}</div>
                <div style="font-size: 14px; font-weight: 800; color: {p_color}; text-align: left;">{p_code}</div>
                <div style="font-size: 13px; font-weight: 600; color: #1C1C1E; text-align: left; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{p_result}</div>
                <div style="font-size: 13px; font-weight: 700; color: #1C1C1E;">{p_velo}</div>
                <div><span style="font-size: 12px; font-weight: 800; color: #1C1C1E; background-color: #E5E5EA; border-radius: 4px; padding: 2px 6px;">--</span></div>
            </div>
            """
            
        if not pitch_sequence_html:
            pitch_sequence_html = "<div style='padding: 10px; color: #8E8E93; font-size: 13px; font-style: italic;'>No pitch data available.</div>"
            
    else:
        st.warning("No play-by-play data available for this game.")
        batter_name, pitcher_name, inning, outs, away_score, home_score, away_abbr, home_abbr = "N/A", "N/A", "-", 0, 0, 0, "AWY", "HME"
        inning_summary_html = ""
        pitch_sequence_html = ""
        plot_pitches = []

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

                <div style="border-left: 1px solid #E5E5EA; padding: 10px 20px; display: flex; flex-direction: column; min-width: 320px; background-color: #FAFAFA; overflow-y: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div style="font-size: 11px; font-weight: 800; color: #8E8E93; text-transform: uppercase;">Inning Summary</div>
                        <div style="display: flex; gap: 15px; text-align: right;">
                            <div style="font-size: 11px; font-weight: 700; color: #8E8E93; width: 35px;">EV</div>
                            <div style="font-size: 11px; font-weight: 700; color: #8E8E93; width: 35px;">xBA</div>
                        </div>
                    </div>
                    {inning_summary_html}
                </div>
            </div>
            """, height=135)

            st.write("")

            # --- ROW 2: THE LIVE AT-BAT (3 Columns) ---
            action_col1, action_col2, action_col3 = st.columns([1.2, 0.8, 1.2])

            with action_col1:
                st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px;">Pitch Usage</div>', unsafe_allow_html=True)
                # Static placeholder for now, as calculating live usage requires full game parsing
                st.markdown("""
                <div style="background-color: white; border-radius: 12px; padding: 15px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); border: 1px solid #E5E5EA;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; text-align: center; border-bottom: 1px solid #E5E5EA; padding-bottom: 8px; margin-bottom: 8px;">
                        <div style="font-size: 11px; font-weight: 700; color: #8E8E93; text-align: left;">PITCH</div>
                        <div style="font-size: 11px; font-weight: 700; color: #8E8E93;">GAME</div>
                        <div style="font-size: 11px; font-weight: 700; color: #8E8E93;">SEASON</div>
                        <div style="font-size: 11px; font-weight: 700; color: #8E8E93;">VELO</div>
                    </div>
                    <div style="padding: 10px; color: #8E8E93; font-size: 13px; font-style: italic;">Live Usage Feed connecting...</div>
                </div>
                """, unsafe_allow_html=True)

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
                
                # Plot Real Pitches
                for p in plot_pitches:
                    ax.scatter(p['x'], p['z'], color=p['color'], s=200, zorder=5, edgecolor='white', linewidth=1.5)
                    ax.text(p['x'], p['z'], str(p['num']), color='white', fontsize=9, ha='center', va='center', weight='bold', zorder=6)
                    
                ax.axis('off')
                st.pyplot(fig, transparent=True)

            with action_col3:
                st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px;">Pitch Sequence</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background-color: white; border-radius: 12px; padding: 15px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); border: 1px solid #E5E5EA; height: 100%;">
                    <div style="display: grid; grid-template-columns: 0.5fr 1fr 2fr 1fr 1fr; text-align: center; border-bottom: 1px solid #E5E5EA; padding-bottom: 8px; margin-bottom: 8px;">
                        <div style="font-size: 11px; font-weight: 700; color: #8E8E93; text-align: left;">#</div>
                        <div style="font-size: 11px; font-weight: 700; color: #8E8E93; text-align: left;">PITCH</div>
                        <div style="font-size: 11px; font-weight: 700; color: #8E8E93; text-align: left;">RESULT</div>
                        <div style="font-size: 11px; font-weight: 700; color: #8E8E93;">VELO</div>
                        <div style="font-size: 11px; font-weight: 700; color: #8E8E93;">STUFF+</div>
                    </div>
                    {pitch_sequence_html}
                </div>
                """, unsafe_allow_html=True)

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
