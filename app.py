import streamlit as st
import requests
from datetime import datetime
import pytz

# ==========================================
# 1. PAGE SETUP & UI CSS
# ==========================================
st.set_page_config(page_title="Databacks | Home", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
/* Base Theme */
.stApp { background-color: #F2F2F7; color: #1C1C1E; font-family: -apple-system, sans-serif; }
#MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}

/* Core Card Style */
.slick-card { 
    background-color: #FFFFFF; 
    border-radius: 16px; 
    padding: 20px; 
    box-shadow: 0 4px 16px rgba(0,0,0,0.05); 
    border: 1px solid #E5E5EA; 
    margin-bottom: 16px; 
}

/* D-Backs Accent Cards */
.card-red { border-top: 4px solid #A71930; }
.card-teal { border-top: 4px solid #30CED8; }
.card-black { border-top: 4px solid #1C1C1E; }

/* Typography */
.section-title { font-size: 18px; font-weight: 800; color: #1C1C1E; margin-bottom: 12px; }
.sub-text { font-size: 12px; font-weight: 600; color: #8E8E93; text-transform: uppercase; }

/* Stat Row Text */
.stat-shelf { font-size: 11px; color: #8E8E93; display: flex; justify-content: space-between; margin-top: 4px; font-weight: 600; }
.stat-val { color: #1C1C1E; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BACKEND DATA ENGINES (MANAGER'S DESK)
# ==========================================

# Cleaned up! You only type names here now. The API finds their stats automatically.
DEPTH_CHART = {
    "lineup": [
        "1. Corbin Carroll", "2. Ketel Marte", "3. Geraldo Perdomo", 
        "4. Gabriel Moreno", "5. Adrian Del Castillo", "6. Nolan Arenado", 
        "7. Carlos Santana", "8. Alek Thomas", "9. Tim Tawa"
    ],
    "bench": [
        "James McCann", "Jose Fernandez", "Ildemaro Vargas", "Jorge Barrosa"
    ],
    "rotation": [
        "1. Zac Gallen", "2. Ryne Nelson", "3. Eduardo Rodriguez", 
        "4. Michael Soroka", "5. Brandon Pfaadt"
    ],
    "bullpen": [
        "CL - Paul Sewald", "SU - Jonathan Loáisiga", "SU - Juan Morillo", 
        "MID - Taylor Clarke", "MID - Ryan Thompson", "MID - Andrew Hoffmann", 
        "MID - Kevin Ginkel", "LR - Taylor Rashi"
    ],
    "injured": [
        {"name": "Corbin Burnes", "injury": "60-Day IL • Tommy John", "eta": "ETA: July 2026"},
        {"name": "Merrill Kelly", "injury": "15-Day IL • Nerve Irritation", "eta": "ETA: Mid May"},
        {"name": "Jordan Lawlar", "injury": "10-Day IL • Fractured Wrist", "eta": "ETA: Late May"},
        {"name": "Pavin Smith", "injury": "10-Day IL • Elbow", "eta": "ETA: Late April"},
        {"name": "Lourdes Gurriel Jr.", "injury": "10-Day IL • Torn ACL", "eta": "ETA: Out for season"},
        {"name": "A.J. Puk", "injury": "60-Day IL • Tommy John", "eta": "ETA: Aug 2026"},
        {"name": "Justin Martinez", "injury": "60-Day IL • Tommy John", "eta": "ETA: Aug 2026"}
    ]
}

@st.cache_data(ttl=300) 
def fetch_daily_slate():
    az_tz = pytz.timezone('America/Phoenix')
    today = datetime.now(az_tz).strftime('%Y-%m-%d')
    team_ids = {"D-Backs": 109, "Aces (AAA)": 238, "Sod Poodles (AA)": 3251, "Hops (A+)": 425, "Rawhide (A)": 430}
    slate = []
    
    for name, team_id in team_ids.items():
        try:
            url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1,11,12,13,14&teamId={team_id}&date={today}&hydrate=probablePitcher(note)"
            res = requests.get(url, timeout=5).json()
            if res['totalItems'] > 0:
                game = res['dates'][0]['games'][0]
                status = game['status']['detailedState']
                if status == "Scheduled" or status == "Pre-Game":
                    game_time = game['gameDate'].split('T')[1][:5]
                    slate.append({"name": name, "score": f"{game_time} UTC", "hero": "Scheduled"})
                else:
                    away = game['teams']['away'].get('score', 0)
                    home = game['teams']['home'].get('score', 0)
                    slate.append({"name": name, "score": f"{away} - {home} ({status})", "hero": "Live Data"})
            else:
                slate.append({"name": name, "score": "OFF", "hero": "No game today"})
        except:
            slate.append({"name": name, "score": "Error", "hero": "API Failed"})
    return slate

@st.cache_data(ttl=3600) 
def fetch_roster_resource():
    roster_url = "https://statsapi.mlb.com/api/v1/teams/109/roster?rosterType=active"
    try:
        roster_res = requests.get(roster_url, timeout=10).json()
        active_players = {}
        for item in roster_res.get('roster', []):
            active_players[item['person']['fullName']] = item['person']['id']
            
        ids_string = ",".join(str(pid) for pid in active_players.values())
        
        # HYDRATING WITH 'expectedStatistics' PULLS STATCAST DATA LIKE xBA and xwOBA!
        stats_url = f"https://statsapi.mlb.com/api/v1/people?personIds={ids_string}&hydrate=stats(group=[hitting,pitching],type=[season,expectedStatistics])"
        stats_res = requests.get(stats_url, timeout=10).json()
        
        live_stats = {}
        for person in stats_res.get('people', []):
            name = person['fullName']
            stats_list = person.get('stats', [])
            player_data = {}
            for stat_obj in stats_list:
                stat_type = stat_obj['type']['displayName']
                stat_group = stat_obj['group']['displayName']
                s = stat_obj['splits'][0]['stat'] if stat_obj['splits'] else {}
                
                if stat_group == 'hitting':
                    if stat_type == 'season':
                        player_data['avg'] = s.get('avg', '.000')
                        player_data['hr'] = s.get('homeRuns', 0)
                        player_data['rbi'] = s.get('rbi', 0)
                        player_data['ops'] = s.get('ops', '.000')
                    elif stat_type == 'expectedStatistics':
                        player_data['xba'] = s.get('estimatedBa', '---')
                        player_data['xwoba'] = s.get('estimatedWoba', '---')
                        
                elif stat_group == 'pitching':
                    if stat_type == 'season':
                        player_data['era'] = s.get('era', '0.00')
                        player_data['whip'] = s.get('whip', '0.00')
                        player_data['ip'] = s.get('inningsPitched', '0.0')
                        tbf = s.get('battersFaced', 1)
                        k = s.get('strikeOuts', 0)
                        bb = s.get('baseOnBalls', 0)
                        player_data['k'] = f"{int((k / max(tbf, 1)) * 100)}%"
                        player_data['bb'] = f"{int((bb / max(tbf, 1)) * 100)}%"
                    elif stat_type == 'expectedStatistics':
                        player_data['xwoba'] = s.get('estimatedWoba', '---')
                        
            live_stats[name] = player_data
            
        def build_player_dict(raw_name, p_type="hitter"):
            clean_name = raw_name.split(". ")[-1].split(" - ")[-1]
            p_dict = {"name": raw_name}
            
            s = live_stats.get(clean_name, {})
            
            if p_type == "hitter":
                p_dict['avg'] = s.get('avg', '.000')
                p_dict['hr'] = s.get('hr', '0')
                p_dict['rbi'] = s.get('rbi', '0')
                p_dict['ops'] = s.get('ops', '.000')
                p_dict['xba'] = str(s.get('xba', '---')).lstrip('0') # formatting decimals
                p_dict['xwoba'] = str(s.get('xwoba', '---')).lstrip('0')
            elif p_type == "pitcher":
                p_dict['era'] = s.get('era', '0.00')
                p_dict['whip'] = s.get('whip', '0.00')
                p_dict['ip'] = s.get('ip', '0.0')
                p_dict['k'] = s.get('k', '0%')
                p_dict['bb'] = s.get('bb', '0%')
                p_dict['xwoba'] = str(s.get('xwoba', '---')).lstrip('0')
            
            if clean_name not in active_players:
                p_dict["name"] += " <span style='color: #FF3B30; font-size: 10px;'>🔴 IL/MINORS</span>"
            return p_dict
            
        return {
            "status": "Success",
            "lineup": [build_player_dict(p, "hitter") for p in DEPTH_CHART["lineup"]],
            "bench": [build_player_dict(p, "hitter") for p in DEPTH_CHART["bench"]],
            "rotation": [build_player_dict(p, "pitcher") for p in DEPTH_CHART["rotation"]],
            "bullpen": [build_player_dict(p, "pitcher") for p in DEPTH_CHART["bullpen"]],
            "injured": DEPTH_CHART["injured"]
        }
        
    except Exception as e:
        # Failsafe dummy data generator so the UI never crashes
        def dummy(n): return {"name": n, "avg": "---", "hr": "-", "rbi": "-", "ops": "---", "xba": "---", "xwoba": "---", "era": "---", "whip": "---", "ip": "---", "k": "-", "bb": "-"}
        return {
            "status": "Offline",
            "lineup": [dummy(p) for p in DEPTH_CHART["lineup"]], "bench": [dummy(p) for p in DEPTH_CHART["bench"]],
            "rotation": [dummy(p) for p in DEPTH_CHART["rotation"]], "bullpen": [dummy(p) for p in DEPTH_CHART["bullpen"]],
            "injured": DEPTH_CHART["injured"]
        }

live_slate = fetch_daily_slate()
roster_data = fetch_roster_resource()

# ==========================================
# 3. FRONTEND UI RENDERING
# ==========================================

az_tz = pytz.timezone('America/Phoenix')
display_date = datetime.now(az_tz).strftime("%B %d, %Y")
st.markdown(f'<div class="section-title">The Daily Slate ({display_date})</div>', unsafe_allow_html=True)
slate_cols = st.columns(5)

for col, team in zip(slate_cols, live_slate):
    with col:
        html_card = f'<div class="slick-card" style="text-align: center; padding: 15px;"><div class="sub-text">{team["name"]}</div><div style="font-size: 16px; font-weight: 800; margin: 8px 0;">{team["score"]}</div><div style="font-size: 12px; color: #8E8E93; font-weight: 500;">{team["hero"]}</div></div>'
        st.markdown(html_card, unsafe_allow_html=True)

st.markdown('<div class="section-title">Player Spotlight</div>', unsafe_allow_html=True)
spotlight_html = (
    '<div class="slick-card">'
    '<div style="display: flex; align-items: center; gap: 30px;">'
    '<div style="width: 100px; height: 100px; background-color: #E5E5EA; border-radius: 50%; display: flex; align-items: center; justify-content: center;"><span style="font-size: 30px;">📸</span></div>'
    '<div style="flex-grow: 1;">'
    '<div class="sub-text">STARTING PITCHER • TODAY</div>'
    '<div style="font-size: 24px; font-weight: 800; margin-bottom: 5px;">Zac Gallen</div>'
    '<div style="display: flex; gap: 20px;">'
    '<div><span class="sub-text">ERA</span> <span style="font-weight: 700;">3.12</span></div>'
    '<div><span class="sub-text">FIP</span> <span style="font-weight: 700;">3.40</span></div>'
    '</div></div></div></div>'
)
st.markdown(spotlight_html, unsafe_allow_html=True)

col_hitters, col_pitchers, col_il = st.columns(3)

def build_hitter_html(title, players):
    items = f'<div style="padding: 10px; background-color: #F9F9F9; border-bottom: 1px solid #E5E5EA; font-weight: 800; font-size: 14px; color: #A71930;">{title}</div>'
    for p in players:
        items += f'<div style="padding: 10px; border-bottom: 1px solid #E5E5EA;"><div style="font-size: 14px; font-weight: 700; margin-bottom: 2px; color: #1C1C1E;">{p["name"]}</div><div class="stat-shelf"><span>AVG <span class="stat-val">{p["avg"]}</span></span><span>HR <span class="stat-val">{p["hr"]}</span></span><span>RBI <span class="stat-val">{p["rbi"]}</span></span><span>OPS <span class="stat-val">{p["ops"]}</span></span><span>xBA <span class="stat-val">{p["xba"]}</span></span><span>xwOBA <span class="stat-val">{p["xwoba"]}</span></span></div></div>'
    return f'<div class="slick-card card-red" style="padding: 0px; overflow: hidden;">{items}</div>'

def build_pitcher_html(title, players):
    items = f'<div style="padding: 10px; background-color: #F9F9F9; border-bottom: 1px solid #E5E5EA; font-weight: 800; font-size: 14px; color: #30CED8;">{title}</div>'
    for p in players:
        items += f'<div style="padding: 10px; border-bottom: 1px solid #E5E5EA;"><div style="font-size: 14px; font-weight: 700; margin-bottom: 2px; color: #1C1C1E;">{p["name"]}</div><div class="stat-shelf"><span>ERA <span class="stat-val">{p["era"]}</span></span><span>WHIP <span class="stat-val">{p["whip"]}</span></span><span>IP <span class="stat-val">{p["ip"]}</span></span><span>K% <span class="stat-val">{p["k"]}</span></span><span>BB% <span class="stat-val">{p["bb"]}</span></span><span>xwOBA <span class="stat-val">{p["xwoba"]}</span></span></div></div>'
    return f'<div class="slick-card card-teal" style="padding: 0px; overflow: hidden;">{items}</div>'

def build_il_html(title, players):
    items = f'<div style="padding: 10px; background-color: #F9F9F9; border-bottom: 1px solid #E5E5EA; font-weight: 800; font-size: 14px; color: #1C1C1E;">{title}</div>'
    for p in players:
        items += f'<div style="padding: 10px; border-bottom: 1px solid #E5E5EA;"><div style="font-size: 14px; font-weight: 700; margin-bottom: 2px; color: #1C1C1E;">{p["name"]}</div><div style="font-size: 11px; color: #8E8E93;">{p["injury"]}</div><div style="font-size: 11px; color: #D22D49; font-weight: 600; margin-top: 2px;">{p["eta"]}</div></div>'
    return f'<div class="slick-card card-black" style="padding: 0px; overflow: hidden;">{items}</div>'

with col_hitters:
    st.markdown(build_hitter_html("Projected Lineup", roster_data['lineup']), unsafe_allow_html=True)
    st.markdown(build_hitter_html("Bench", roster_data['bench']), unsafe_allow_html=True)

with col_pitchers:
    st.markdown(build_pitcher_html("Starting Rotation", roster_data['rotation']), unsafe_allow_html=True)
    st.markdown(build_pitcher_html("Bullpen", roster_data['bullpen']), unsafe_allow_html=True)

with col_il:
    st.markdown(build_il_html("Injured List", roster_data['injured']), unsafe_allow_html=True)
