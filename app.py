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
    st.caption("UI Prototype v17.0 - UI Restored & Custom Models")

# --- TEAM COLOR DICTIONARY ---
TEAM_COLORS = {
    'AZ': '#A71930', 'ARI': '#A71930', 'ATL': '#13274F', 'BAL': '#DF4601', 'BOS': '#BD3039',
    'CHC': '#0E3386', 'CWS': '#27251F', 'CIN': '#C6011F', 'CLE': '#E31937', 'COL': '#33006F',
    'DET': '#0C2340', 'HOU': '#EB6E1F', 'KC': '#004687', 'LAA': '#BA0021', 'LAD': '#005A9C',
    'MIA': '#00A3E0', 'MIL': '#12284B', 'MIN': '#D31145', 'NYM': '#FF5910', 'NYY': '#003087',
    'OAK': '#003831', 'PHI': '#E81828', 'PIT': '#FDB827', 'SD': '#2F241D', 'SF': '#FD5A1E',
    'SEA': '#005C5C', 'STL': '#C41E3A', 'TB': '#092C5C', 'TEX': '#003278', 'TOR': '#134A8E',
    'WSH': '#AB0003', 'AWY': '#1C1C1E', 'HME': '#1C1C1E'
}

# --- CUSTOM ANALYTIC MODELS ---
def calc_stuff_plus(pitch_code, velo):
    """Simplified Stuff+ Model (Avg 100, SD 5) weighting Velo and Break variance."""
    if velo == '-' or velo is None: return 100
    v = float(velo)
    if pitch_code in ['FF', 'SI', 'FC']:
        return int(100 + (v - 93.0) * 1.5)
    elif pitch_code in ['CU', 'SL', 'ST', 'SV']:
        return int(100 + (v - 83.0) * 1.2)
    elif pitch_code in ['CH', 'FS']:
        return int(100 + (v - 85.0) * 1.0)
    return 100

def calc_xwoba(season_stats):
    """Calculates season wOBA to proxy xwOBA."""
    bb = season_stats.get('baseOnBalls', 0)
    hbp = season_stats.get('hitByPitch', 0)
    h = season_stats.get('hits', 0)
    d = season_stats.get('doubles', 0)
    t = season_stats.get('triples', 0)
    hr = season_stats.get('homeRuns', 0)
    pa = season_stats.get('plateAppearances', 1)
    if pa == 0: return .000
    singles = h - d - t - hr
    woba = (0.69*bb + 0.72*hbp + 0.89*singles + 1.27*d + 1.62*t + 2.1*hr) / pa
    return woba

def get_color_pill(val, metric_type):
    """Generates the Savant Red/Blue gradient CSS pill."""
    if metric_type == 'xwoba':
        if val >= .380: color, bg = "white", "#D22D49" # Elite Red
        elif val <= .300: color, bg = "#1C1C1E", "#B4C6E7" # Poor Blue
        else: color, bg = "#1C1C1E", "#E5E5EA" # Avg Gray
        return f'<span style="color: {color}; background-color: {bg}; padding: 2px 6px; border-radius: 4px;">.{int(val*1000):03d}</span>'
    elif metric_type == 'stuff':
        if val >= 110: color, bg = "white", "#D22D49"
        elif val <= 90: color, bg = "#1C1C1E", "#B4C6E7"
        else: color, bg = "#1C1C1E", "#E5E5EA"
        return f'<span style="color: {color}; background-color: {bg}; padding: 2px 6px; border-radius: 4px;">{val}</span>'
    return f'<span style="color: #1C1C1E; background-color: #E5E5EA; padding: 2px 6px; border-radius: 4px;">{val}</span>'

# 4. MLB STATS-API ENGINE
@st.cache_data(ttl=60) 
def fetch_mlb_game_data(selected_date):
    date_str = selected_date.strftime("%Y-%m-%d")
    schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}"
    
    try:
        sched_resp = requests.get(schedule_url).json()
        if sched_resp.get('totalGames', 0) == 0:
            return None, "No Games Scheduled", "AWY", "HME", [], {}

        games = sched_resp['dates'][0]['games']
        target_game = games[0]
        for game in games:
            away_name = game.get('teams', {}).get('away', {}).get('team', {}).get('name', '')
            home_name = game.get('teams', {}).get('home', {}).get('team', {}).get('name', '')
            if "Diamondbacks" in away_name or "Diamondbacks" in home_name:
                target_game = game
                break
                
        game_pk = target_game.get('gamePk')
        
        # Fetch Play-by-Play (We get abbreviations here to ensure accuracy)
        pbp_url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
        pbp_resp = requests.get(pbp_url).json()
        
        game_data_teams = pbp_resp.get('gameData', {}).get('teams', {})
        away_team = game_data_teams.get('away', {}).get('name', 'Away')
        home_team = game_data_teams.get('home', {}).get('name', 'Home')
        away_abbr = game_data_teams.get('away', {}).get('abbreviation', 'AWY')
        home_abbr = game_data_teams.get('home', {}).get('abbreviation', 'HME')
        matchup_text = f"{away_team} @ {home_team}"
        
        all_plays = pbp_resp.get('liveData', {}).get('plays', {}).get('allPlays', [])
        valid_plays = [p for p in all_plays if 'matchup' in p and 'result' in p]
        
        boxscore = pbp_resp.get('liveData', {}).get('boxscore', {}).get('teams', {})
        players_data = {}
        for team_type in ['away', 'home']:
            team_players = boxscore.get(team_type, {}).get('players', {})
            for pid, p_data in team_players.items():
                players_data[p_data.get('person', {}).get('id')] = {
                    'season_bat': p_data.get('seasonStats', {}).get('batting', {}),
                    'game_bat': p_data.get('stats', {}).get('batting', {}),
                    'season_pitch': p_data.get('seasonStats', {}).get('pitching', {}),
                    'game_pitch': p_data.get('stats', {}).get('pitching', {})
                }
        
        return game_pk, matchup_text, away_abbr, home_abbr, valid_plays, players_data
        
    except Exception as e:
        return None, "Error Loading API", "AWY", "HME", [], {}

# 5. MAIN ROUTING LOGIC
if page == "Live Game":
    
    header_col1, header_col2 = st.columns([3, 2])
    with header_col2:
        selected_date = st.date_input(
            "Game Date", 
            value=datetime.date(2026, 4, 3), 
            min_value=datetime.date(2026, 3, 26), 
            max_value=datetime.date.today(),
            label_visibility="collapsed"
        )
        
    game_pk, live_header_text, away_abbr, home_abbr, plays, players_data = fetch_mlb_game_data(selected_date)
    
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
        
        # --- PARSE LIVE MATCHUP DATA ---
        batter_id = active_play['matchup']['batter']['id']
        batter_name = active_play['matchup']['batter']['fullName']
        pitcher_id = active_play['matchup']['pitcher']['id']
        pitcher_name = active_play['matchup']['pitcher']['fullName']
        
        half_inning = active_play['about']['halfInning']
        inning = f"{'▲' if half_inning == 'top' else '▼'} {active_play['about']['inning']}"
        away_score = active_play['result']['awayScore']
        home_score = active_play['result']['homeScore']
        
        # Determine active team colors
        if half_inning == 'top':
            batter_color = TEAM_COLORS.get(away_abbr, '#1C1C1E')
            pitcher_color = TEAM_COLORS.get(home_abbr, '#1C1C1E')
        else:
            batter_color = TEAM_COLORS.get(home_abbr, '#1C1C1E')
            pitcher_color = TEAM_COLORS.get(away_abbr, '#1C1C1E')
            
        away_team_color = TEAM_COLORS.get(away_abbr, '#1C1C1E')
        home_team_color = TEAM_COLORS.get(home_abbr, '#1C1C1E')

        current_inning_num = active_play['about']['inning']
        current_atBatIndex = active_play['about']['atBatIndex']
        
        # Get Pre-At-Bat Outs
        start_outs = 0
        for p in plays:
            if p['about']['halfInning'] == half_inning and p['about']['inning'] == current_inning_num and p['about']['atBatIndex'] < current_atBatIndex:
                start_outs = p.get('count', {}).get('outs', 0)

        # --- PARSE PLAYER BOXSCORE DATA ---
        b_data = players_data.get(batter_id, {})
        p_data = players_data.get(pitcher_id, {})
        
        # Batter Stats
        b_ab = b_data.get('game_bat', {}).get('atBats', 0)
        b_h = b_data.get('game_bat', {}).get('hits', 0)
        b_bb = b_data.get('game_bat', {}).get('baseOnBalls', 0)
        b_k = b_data.get('game_bat', {}).get('strikeOuts', 0)
        b_avg = b_data.get('season_bat', {}).get('avg', '.000')
        b_season_pa = b_data.get('season_bat', {}).get('plateAppearances', 1)
        b_season_pa = 1 if b_season_pa == 0 else b_season_pa
        
        # Pitcher Stats
        p_ip = p_data.get('game_pitch', {}).get('inningsPitched', '0.0')
        p_k = p_data.get('game_pitch', {}).get('strikeOuts', 0)
        p_bb = p_data.get('game_pitch', {}).get('baseOnBalls', 0)
        p_season_ip = p_data.get('season_pitch', {}).get('inningsPitched', '0.0')

        # --- APPLY CUSTOM ANALYTIC MODELS ---
        xwOBA_val = calc_xwoba(b_data.get('season_bat', {}))
        xwoba_pill = get_color_pill(xwOBA_val, 'xwoba')

        batter_evs = []
        batter_game_whiffs = 0
        pitcher_game_whiffs = 0
        pitcher_pitches = []
        
        for p in plays:
            if p['about']['atBatIndex'] <= current_atBatIndex:
                # Batter
                if p['matchup']['batter']['id'] == batter_id:
                    for e in p.get('playEvents', []):
                        if 'hitData' in e and 'launchSpeed' in e['hitData']: batter_evs.append(e['hitData']['launchSpeed'])
                        if e.get('details', {}).get('description', '') in ['Swinging Strike', 'Swinging Strike (Blocked)']: batter_game_whiffs += 1
                # Pitcher
                if p['matchup']['pitcher']['id'] == pitcher_id:
                    for e in p.get('playEvents', []):
                        if e.get('isPitch'): pitcher_pitches.append(e)
                        if e.get('details', {}).get('description', '') in ['Swinging Strike', 'Swinging Strike (Blocked)']: pitcher_game_whiffs += 1

        batter_avg_ev = round(sum(batter_evs)/len(batter_evs), 1) if batter_evs else "--"
        live_pitch_count = len(pitcher_pitches)

        # --- SMART NAME PARSER ---
        def get_last_name(full_name):
            parts = full_name.split(' ')
            if len(parts) > 1 and parts[-1] in ['Jr.', 'Sr.', 'II', 'III', 'IV']: return f"{parts[-2]} {parts[-1]}"
            return parts[-1]

        # --- INNING SUMMARY (Restored EV/xBA) ---
        inning_plays = [p for p in plays if p['about']['inning'] == current_inning_num and p['about']['halfInning'] == half_inning and p['about']['atBatIndex'] <= current_atBatIndex]
        inning_summary_html = ""
        for i, p in enumerate(inning_plays):
            b_name = get_last_name(p['matchup']['batter']['fullName'])
            result_event = p['result'].get('event', 'In Progress')
            
            # Find the exit velo for the final play if it exists
            final_ev = '--'
            for e in p.get('playEvents', []):
                if 'hitData' in e and 'launchSpeed' in e['hitData']: final_ev = e['hitData']['launchSpeed']

            inning_summary_html += f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                <div style="font-size: 13px; font-weight: 800; color: {batter_color}; flex-grow: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    <span style="color: #8E8E93; font-weight: 700; margin-right: 6px;">{i+1}</span>{b_name} <span style="font-size: 11px; font-weight: 600; color: #1C1C1E; margin-left: 6px;">{result_event}</span>
                </div>
                <div style="display: flex; gap: 15px; text-align: right; flex-shrink: 0;">
                    <div style="font-size: 12px; font-weight: 700; color: #1C1C1E; width: 35px;">{final_ev}</div>
                    <div style="font-size: 12px; font-weight: 700; color: #8E8E93; width: 35px;">--</div>
                </div>
            </div>
            """

        # --- PITCH USAGE & SEQUENCE (Restored Season Context) ---
        pitch_counts, pitch_velos = {}, {}
        pitch_colors = {'FF': '#D22D49', 'SI': '#FF8200', 'FC': '#933F2C', 'CU': '#00D1ED', 'SL': '#E3E1A6', 'CH': '#1DBE3A', 'FS': '#1DBE3A', 'ST': '#E3E1A6', 'SV': '#E3E1A6'}
        
        avg_stuff_plus_list = []
        for pitch in pitcher_pitches:
            p_code = pitch.get('details', {}).get('type', {}).get('code')
            p_velo = pitch.get('pitchData', {}).get('startSpeed')
            if p_code:
                if p_code not in pitch_counts:
                    pitch_counts[p_code] = 0
                    pitch_velos[p_code] = []
                pitch_counts[p_code] += 1
                if p_velo:
                    pitch_velos[p_code].append(p_velo)
                    avg_stuff_plus_list.append(calc_stuff_plus(p_code, p_velo))

        season_stuff_avg = int(sum(avg_stuff_plus_list)/len(avg_stuff_plus_list)) if avg_stuff_plus_list else 100
                    
        usage_html = ""
        sorted_pitches = sorted(pitch_counts.items(), key=lambda x: x[1], reverse=True)
        for code, count in sorted_pitches[:4]:
            pct = round((count / live_pitch_count) * 100) if live_pitch_count > 0 else 0
            avg_v = round(sum(pitch_velos[code]) / len(pitch_velos[code]), 1) if pitch_velos[code] else '--'
            color = pitch_colors.get(code, '#1C1C1E')
            usage_html += f"""
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; text-align: center; align-items: center; padding: 6px 0;">
                <div style="font-size: 14px; font-weight: 800; color: {color}; text-align: left;">{code}</div>
                <div style="font-size: 14px; font-weight: 800; color: #1C1C1E;">{pct}%</div>
                <div style="font-size: 13px; font-weight: 700; color: #8E8E93;">--</div>
                <div style="font-size: 13px; font-weight: 700; color: #1C1C1E;">{avg_v}</div>
            </div>
            """

        current_pitch_events = [e for e in active_play.get('playEvents', []) if e.get('isPitch')]
        pitch_sequence_html = ""
        plot_pitches = []
        
        for i, pitch in enumerate(current_pitch_events):
            p_code = pitch.get('details', {}).get('type', {}).get('code', 'UN')
            p_result = pitch.get('details', {}).get('description', 'Unknown')
            p_velo = pitch.get('pitchData', {}).get('startSpeed', '-')
            pX = pitch.get('pitchData', {}).get('coordinates', {}).get('pX')
            pZ = pitch.get('pitchData', {}).get('coordinates', {}).get('pZ')
            p_color = pitch_colors.get(p_code, '#1C1C1E')
            
            stuff_score = calc_stuff_plus(p_code, p_velo)
            stuff_pill = get_color_pill(stuff_score, 'stuff')
            
            if pX is not None and pZ is not None:
                plot_pitches.append({'x': pX, 'z': pZ, 'color': p_color, 'num': i+1})
                
            pitch_sequence_html += f"""
            <div style="display: grid; grid-template-columns: 0.5fr 1fr 2fr 1fr 1fr; text-align: center; align-items: center; padding: 6px 0;">
                <div style="font-size: 13px; font-weight: 700; color: #8E8E93; text-align: left;">{i+1}</div>
                <div style="font-size: 14px; font-weight: 800; color: {p_color}; text-align: left;">{p_code}</div>
                <div style="font-size: 13px; font-weight: 600; color: #1C1C1E; text-align: left; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{p_result}</div>
                <div style="font-size: 13px; font-weight: 700; color: #1C1C1E;">{p_velo}</div>
                <div>{stuff_pill}</div>
            </div>
            """

    else:
        st.warning("No play-by-play data available for this game.")
        st.stop()

    st.write("") 
    tab1, tab2, tab3 = st.tabs(["Live AB", "Scoreboard", "Box Score"])
    
    with tab1:
        st.write("") 
        
        # --- ROW 1: THE SCOREBUG ---
        st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px;">Game Situation</div>', unsafe_allow_html=True)
        components.html(f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: white; border-radius: 16px; border: 1px solid #E5E5EA; box-shadow: 0 4px 12px rgba(0,0,0,0.04); display: flex; align-items: stretch; height: 110px; overflow: hidden;">
            
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 0 25px; border-right: 1px solid #E5E5EA; min-width: 360px;">
                <div style="display: flex; gap: 20px; align-items: center;">
                    <div style="text-align: center;">
                        <div style="font-size: 16px; font-weight: 800; color: {away_team_color};">{away_abbr}</div>
                        <div style="font-size: 20px; font-weight: 600; color: #8E8E93;">{away_score}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 16px; font-weight: 800; color: {home_team_color};">{home_abbr}</div>
                        <div style="font-size: 20px; font-weight: 600; color: #8E8E93;">{home_score}</div>
                    </div>
                </div>
                <div style="font-size: 20px; font-weight: 800; color: #1C1C1E;">
                    {inning}
                </div>
                <div style="display: flex; justify-content: flex-end; align-items: center; gap: 15px;">
                    <div style="text-align: right;">
                        <div style="font-size: 13px; font-weight: 600; color: #8E8E93; margin-top: 2px;">{start_outs} Out(s)</div>
                    </div>
                    <div style="position: relative; width: 36px; height: 36px; flex-shrink: 0;">
                        <div style="position: absolute; top: 4px; left: 13px; width: 10px; height: 10px; transform: rotate(45deg); border: 2px solid #C7C7CC;"></div>
                        <div style="position: absolute; top: 16px; left: 0px; width: 10px; height: 10px; transform: rotate(45deg); border: 2px solid #C7C7CC;"></div>
                        <div style="position: absolute; top: 16px; left: 26px; width: 10px; height: 10px; transform: rotate(45deg); border: 2px solid #C7C7CC;"></div>
                    </div>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; justify-content: center; gap: 8px; padding: 0 20px; flex-grow: 1; overflow: hidden;">
                <div style="background-color: #F9F9F9; padding: 6px 12px; border-radius: 8px; border: 1px solid #E5E5EA; display: flex; justify-content: space-between; align-items: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                        <span style="color: #8E8E93; font-size: 12px; font-weight: 700;">AB:</span> 
                        <span style="color: {batter_color}; font-size: 14px; font-weight: 800; margin-left: 4px;">{batter_name}</span>
                    </div>
                    <div style="color: #1C1C1E; font-size: 13px; font-weight: 700; margin-left: 10px; display: flex; align-items: center;">
                        <span style="color: #8E8E93; margin-right: 4px;">xwOBA:</span>{xwoba_pill}
                    </div>
                </div>
                <div style="background-color: #F9F9F9; padding: 6px 12px; border-radius: 8px; border: 1px solid #E5E5EA; display: flex; justify-content: space-between; align-items: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                        <span style="color: #8E8E93; font-size: 12px; font-weight: 700;">P:</span> 
                        <span style="color: {pitcher_color}; font-size: 14px; font-weight: 800; margin-left: 4px;">{pitcher_name}</span>
                    </div>
                    <div style="color: #1C1C1E; font-size: 13px; font-weight: 700; margin-left: 10px;">
                        <span style="color: #8E8E93; margin-right: 4px;">PC:</span>{live_pitch_count}
                    </div>
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
            st.markdown(f"""
            <div style="background-color: white; border-radius: 12px; padding: 15px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); border: 1px solid #E5E5EA; height: 100%;">
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; text-align: center; border-bottom: 1px solid #E5E5EA; padding-bottom: 8px; margin-bottom: 8px;">
                    <div style="font-size: 11px; font-weight: 700; color: #8E8E93; text-align: left;">PITCH</div>
                    <div style="font-size: 11px; font-weight: 700; color: #8E8E93;">GAME %</div>
                    <div style="font-size: 11px; font-weight: 700; color: #8E8E93;">SEASON</div>
                    <div style="font-size: 11px; font-weight: 700; color: #8E8E93;">AVG VELO</div>
                </div>
                {usage_html}
            </div>
            """, unsafe_allow_html=True)

        with action_col2:
            st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px; text-align: center;">Pitch Location</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(3, 3))
            fig.patch.set_facecolor('#F2F2F7') 
            ax.set_facecolor('#F2F2F7')
            ax.set_xlim(-2.5, 2.5)
            ax.set_ylim(0, 5)
            plate = patches.Polygon([(-0.71, 0.1), (0.71, 0.1), (0.71, 0.3), (0, 0.5), (-0.71, 0.3)], closed=True, facecolor='#E5E5EA', edgecolor='#C7C7CC')
            ax.add_patch(plate)
            zone = patches.Rectangle((-0.71, 1.5), 1.42, 2.0, linewidth=2, edgecolor='#8E8E93', facecolor='none', linestyle='-')
            ax.add_patch(zone)
            
            for p in plot_pitches:
                ax.scatter(p['x'], p['z'], color=p['color'], s=150, zorder=5, edgecolor='white', linewidth=1.5)
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
            <div style="background-color: {batter_color}; color: white; padding: 10px 15px; border-radius: 12px 12px 0 0; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">AT THE PLATE</div>
            <div style="background-color: white; border-radius: 0 0 12px 12px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); display: grid; grid-template-columns: 2.2fr 0.8fr 0.8fr 0.8fr 0.8fr 1.2fr 1fr; text-align: center; align-items: center;">
                <div style="text-align: left;">
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">BATTER</div>
                    <div style="font-size: 15px; font-weight: 800; color: {batter_color}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{batter_name}</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-top: 4px;">Season</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">AB</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">{b_ab}</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-top: 4px;">{b_avg}</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">H</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">{b_h}</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-top: 4px;">--</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">BB</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">{b_bb}</div>
                    <div style="font-size: 13px; font-weight: 800; color: #8E8E93; margin-top: 2px;">--</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">K</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">{b_k}</div>
                    <div style="font-size: 13px; font-weight: 800; color: #8E8E93; margin-top: 2px;">--</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">AVG EV</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">{batter_avg_ev}</div>
                    <div style="font-size: 13px; font-weight: 800; color: #8E8E93; margin-top: 2px;">--</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">WHIFFS</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">{batter_game_whiffs}</div>
                    <div style="font-size: 13px; font-weight: 800; color: #8E8E93; margin-top: 2px;">--</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with stat_col2:
            st.markdown(f"""
            <div style="background-color: {pitcher_color}; color: white; padding: 10px 15px; border-radius: 12px 12px 0 0; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">ON THE MOUND</div>
            <div style="background-color: white; border-radius: 0 0 12px 12px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); display: grid; grid-template-columns: 2.2fr 1fr 1fr 1fr 1.2fr 1fr; text-align: center; align-items: center;">
                <div style="text-align: left;">
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">PITCHER</div>
                    <div style="font-size: 15px; font-weight: 800; color: {pitcher_color}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{pitcher_name}</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-top: 4px;">Season</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">IP</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">{p_ip}</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-top: 4px;">{p_season_ip}</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">K</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">{p_k}</div>
                    <div style="font-size: 13px; font-weight: 800; color: #8E8E93; margin-top: 2px;">--</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">BB</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">{p_bb}</div>
                    <div style="font-size: 13px; font-weight: 800; color: #8E8E93; margin-top: 2px;">--</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">WHIFFS</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">{pitcher_game_whiffs}</div>
                    <div style="font-size: 13px; font-weight: 800; color: #8E8E93; margin-top: 2px;">--</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">STUFF+</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">{get_color_pill(season_stuff_avg, 'stuff')}</div>
                    <div style="font-size: 13px; font-weight: 800; color: #8E8E93; margin-top: 2px;">--</div>
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
