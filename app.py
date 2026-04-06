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

DEPTH_CHART = {
    "lineup": [
        {"name": "1. Corbin Carroll", "avg": ".285", "hr": 2, "rbi": 5, "ops": ".890", "wrc": 135, "war": 0.4},
        {"name": "2. Ketel Marte", "avg": ".310", "hr": 3, "rbi": 8, "ops": ".945", "wrc": 150, "war": 0.6},
        {"name": "3. Geraldo Perdomo", "avg": ".250", "hr": 0, "rbi": 2, "ops": ".710", "wrc": 95, "war": 0.1},
        {"name": "4. Gabriel Moreno", "avg": ".295", "hr": 1, "rbi": 7, "ops": ".820", "wrc": 115, "war": 0.3},
        {"name": "5. Adrian Del Castillo", "avg": ".220", "hr": 1, "rbi": 3, "ops": ".680", "wrc": 88, "war": 0.0},
        {"name": "6. Nolan Arenado", "avg": ".265", "hr": 2, "rbi": 6, "ops": ".790", "wrc": 105, "war": 0.2},
        {"name": "7. Carlos Santana", "avg": ".240", "hr": 1, "rbi": 4, "ops": ".740", "wrc": 102, "war": 0.1},
        {"name": "8. Alek Thomas", "avg": ".270", "hr": 0, "rbi": 1, "ops": ".705", "wrc": 90, "war": 0.1},
        {"name": "9. Tim Tawa", "avg": ".210", "hr": 0, "rbi": 0, "ops": ".600", "wrc": 70, "war": -0.1}
    ],
    "bench": [
        {"name": "James McCann", "avg": ".200", "hr": 0, "rbi": 1, "ops": ".550", "wrc": 60, "war": 0.0},
        {"name": "Jose Fernandez", "avg": ".000", "hr": 0, "rbi": 0, "ops": ".000", "wrc": 0, "war": 0.0},
        {"name": "Ildemaro Vargas", "avg": ".250", "hr": 0, "rbi": 0, "ops": ".650", "wrc": 85, "war": 0.0},
        {"name": "Jorge Barrosa", "avg": ".222", "hr": 0, "rbi": 2, "ops": ".620", "wrc": 80, "war": 0.0}
    ],
    "rotation": [
        {"name": "1. Zac Gallen", "era": "3.12", "whip": "1.05", "k": "26%", "bb": "6%", "fip": "3.40", "war": 0.4},
        {"name": "2. Ryne Nelson", "era": "4.20", "whip": "1.25", "k": "20%", "bb": "8%", "fip": "4.15", "war": 0.1},
        {"name": "3. Eduardo Rodriguez", "era": "3.85", "whip": "1.18", "k": "22%", "bb": "7%", "fip": "3.90", "war": 0.2},
        {"name": "4. Michael Soroka", "era": "4.05", "whip": "1.30", "k": "19%", "bb": "9%", "fip": "4.30", "war": 0.1},
        {"name": "5. Brandon Pfaadt", "era": "3.60", "whip": "1.12", "k": "24%", "bb": "5%", "fip": "3.75", "war": 0.3}
    ],
    "bullpen": [
        {"name": "CL - Paul Sewald", "era": "2.10", "whip": "0.95", "k": "31%", "bb": "8%", "fip": "2.80", "war": 0.2},
        {"name": "SU - Jonathan Loáisiga", "era": "2.80", "whip": "1.10", "k": "23%", "bb": "6%", "fip": "3.10", "war": 0.1},
        {"name": "SU - Juan Morillo", "era": "3.20", "whip": "1.15", "k": "25%", "bb": "9%", "fip": "3.40", "war": 0.1},
        {"name": "MID - Taylor Clarke", "era": "4.50", "whip": "1.35", "k": "18%", "bb": "7%", "fip": "4.20", "war": 0.0},
        {"name": "MID - Ryan Thompson", "era": "3.00", "whip": "1.08", "k": "21%", "bb": "5%", "fip": "3.25", "war": 0.1},
        {"name": "MID - Andrew Hoffmann", "era": "4.10", "whip": "1.28", "k": "20%", "bb": "8%", "fip": "4.00", "war": 0.0},
        {"name": "MID - Kevin Ginkel", "era": "2.90", "whip": "1.02", "k": "28%", "bb": "7%", "fip": "2.95", "war": 0.2},
        {"name": "LR - Taylor Rashi", "era": "4.80", "whip": "1.40", "k": "17%", "bb": "10%", "fip": "4.60", "war": -0.1}
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
        stats_url = f"https://statsapi.mlb.com/api/v1/people?personIds={ids_string}&hydrate=stats(group=[hitting,pitching],type=[season])"
        stats_res = requests.get(stats_url, timeout=10).json()
        
        live_stats = {}
        for person in stats_res.get('people', []):
            name = person['fullName']
            stats_list = person.get('stats', [])
            player_data = {}
            for stat_obj in stats_list:
                if stat_obj['type']['displayName'] == 'season':
                    s = stat_obj['splits'][0]['stat'] if stat_obj['splits'] else {}
                    if stat_obj['group']['displayName'] == 'hitting':
                        player_data['avg'] = s.get('avg', '.000')
                        player_data['hr'] = s.get('homeRuns', 0)
                        player_data['rbi'] = s.get('rbi', 0)
                        player_data['ops'] = s.get('ops', '.000')
                    elif stat_obj['group']['displayName'] == 'pitching':
                        player_data['era'] = s.get('era', '0.00')
                        player_data['whip'] = s.get('whip', '0.00')
                        tbf = s.get('battersFaced', 1)
                        k = s.get('strikeOuts', 0)
                        bb = s.get('baseOnBalls', 0)
                        player_data['k'] = f"{int((k / max(tbf, 1)) * 100)}%"
                        player_data['bb'] = f"{int((bb / max(tbf, 1)) * 100)}%"
            live_stats[name] = player_data
            
        def verify_player(p_dict, p_type="hitter"):
            clean_name = p_dict["name"].split(". ")[-1].split(" - ")[-1]
            if clean_name in live_stats and live_stats[clean_name]:
                s = live_stats[clean_name]
                if p_type == "hitter":
                    p_dict['avg'] = s.get('avg', p_dict['avg'])
                    p_dict['hr'] = s.get('hr', p_dict['hr'])
                    p_dict['rbi'] = s.get('rbi', p_dict['rbi'])
                    p_dict['ops'] = s.get('ops', p_dict['ops'])
                elif p_type == "pitcher":
                    p_dict['era'] = s.get('era', p_dict['era'])
                    p_dict['whip'] = s.get('whip', p_dict['whip'])
                    p_dict['k'] = s.get('k', p_dict['k'])
                    p_dict['bb'] = s.get('bb', p_dict['bb'])
            
            if clean_name not in active_players:
                p_dict["name"] += " <span style='color: #FF3B30; font-size: 10px;'>🔴 IL/MINORS</span>"
            return p_dict
            
        return {
            "status": "Success",
            "lineup": [verify_player(p.copy(), "hitter") for p in DEPTH_CHART["lineup"]],
            "bench": [verify_player(p.copy(), "hitter") for p in DEPTH_CHART["bench"]],
            "rotation": [verify_player(p.copy(), "pitcher") for p in DEPTH_CHART["rotation"]],
            "bullpen": [verify_player(p.copy(), "pitcher") for p in DEPTH_CHART["bullpen"]],
            "injured": DEPTH_CHART["injured"]
        }
        
    except Exception as e:
        return {"status": "Offline", **DEPTH_CHART}

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

# 3-Column Layout
col_hitters, col_pitchers, col_il = st.columns(3)

def build_hitter_html(title, players):
    # Added Sedona Red text to the sub-header
    items = f'<div style="padding: 10px; background-color: #F9F9F9; border-bottom: 1px solid #E5E5EA; font-weight: 800; font-size: 14px; color: #A71930;">{title}</div>'
    for p in players:
        items += f'<div style="padding: 10px; border-bottom: 1px solid #E5E5EA;"><div style="font-size: 14px; font-weight: 700; margin-bottom: 2px; color: #1C1C1E;">{p["name"]}</div><div class="stat-shelf"><span>AVG <span class="stat-val">{p["avg"]}</span></span><span>HR <span class="stat-val">{p["hr"]}</span></span><span>RBI <span class="stat-val">{p["rbi"]}</span></span><span>OPS <span class="stat-val">{p["ops"]}</span></span><span>wRC+ <span class="stat-val">{p["wrc"]}</span></span><span>WAR <span class="stat-val">{p["war"]}</span></span></div></div>'
    # Added .card-red class
    return f'<div class="slick-card card-red" style="padding: 0px; overflow: hidden;">{items}</div>'

def build_pitcher_html(title, players):
    # Added Teal text to the sub-header
    items = f'<div style="padding: 10px; background-color: #F9F9F9; border-bottom: 1px solid #E5E5EA; font-weight: 800; font-size: 14px; color: #30CED8;">{title}</div>'
    for p in players:
        items += f'<div style="padding: 10px; border-bottom: 1px solid #E5E5EA;"><div style="font-size: 14px; font-weight: 700; margin-bottom: 2px; color: #1C1C1E;">{p["name"]}</div><div class="stat-shelf"><span>ERA <span class="stat-val">{p["era"]}</span></span><span>WHIP <span class="stat-val">{p["whip"]}</span></span><span>K% <span class="stat-val">{p["k"]}</span></span><span>BB% <span class="stat-val">{p["bb"]}</span></span><span>FIP <span class="stat-val">{p["fip"]}</span></span><span>WAR <span class="stat-val">{p["war"]}</span></span></div></div>'
    # Added .card-teal class
    return f'<div class="slick-card card-teal" style="padding: 0px; overflow: hidden;">{items}</div>'

def build_il_html(title, players):
    # Added Jet Black text to the sub-header
    items = f'<div style="padding: 10px; background-color: #F9F9F9; border-bottom: 1px solid #E5E5EA; font-weight: 800; font-size: 14px; color: #1C1C1E;">{title}</div>'
    for p in players:
        items += f'<div style="padding: 10px; border-bottom: 1px solid #E5E5EA;"><div style="font-size: 14px; font-weight: 700; margin-bottom: 2px; color: #1C1C1E;">{p["name"]}</div><div style="font-size: 11px; color: #8E8E93;">{p["injury"]}</div><div style="font-size: 11px; color: #D22D49; font-weight: 600; margin-top: 2px;">{p["eta"]}</div></div>'
    # Added .card-black class
    return f'<div class="slick-card card-black" style="padding: 0px; overflow: hidden;">{items}</div>'

# Removed redundant section titles here
with col_hitters:
    st.markdown(build_hitter_html("Projected Lineup", roster_data['lineup']), unsafe_allow_html=True)
    st.markdown(build_hitter_html("Bench", roster_data['bench']), unsafe_allow_html=True)

with col_pitchers:
    st.markdown(build_pitcher_html("Starting Rotation", roster_data['rotation']), unsafe_allow_html=True)
    st.markdown(build_pitcher_html("Bullpen", roster_data['bullpen']), unsafe_allow_html=True)

with col_il:
    st.markdown(build_il_html("Injured List", roster_data['injured']), unsafe_allow_html=True)
