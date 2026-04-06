import streamlit as st
import pandas as pd
import cloudscraper
import requests
from datetime import datetime
import pytz

# ==========================================
# 1. PAGE SETUP & UI CSS
# ==========================================
st.set_page_config(page_title="Databacks | Home", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp { background-color: #F2F2F7; color: #1C1C1E; font-family: -apple-system, sans-serif; }
#MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}

.slick-card { background-color: #FFFFFF; border-radius: 16px; padding: 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.05); border: 1px solid #E5E5EA; margin-bottom: 16px; }
.section-title { font-size: 18px; font-weight: 800; color: #1C1C1E; margin-bottom: 12px; }
.sub-text { font-size: 12px; font-weight: 600; color: #8E8E93; text-transform: uppercase; }

/* Scrollable Container for Roster Columns */
.scrollable-roster { max-height: 350px; overflow-y: auto; padding-right: 5px; }
/* Hide ugly scrollbar but keep functionality */
.scrollable-roster::-webkit-scrollbar { width: 4px; }
.scrollable-roster::-webkit-scrollbar-thumb { background-color: #E5E5EA; border-radius: 4px; }

.bar-bg { background-color: #E5E5EA; border-radius: 8px; height: 8px; width: 100%; margin-top: 4px; }
.bar-red { background-color: #D22D49; border-radius: 8px; height: 100%; }
.bar-blue { background-color: #3B71CA; border-radius: 8px; height: 100%; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BACKEND DATA ENGINES (MANAGER'S DESK)
# ==========================================
# Manually control the exact roster structure based on FanGraphs RosterResource
DEPTH_CHART = {
    "lineup": [
        "1. Corbin Carroll",
        "2. Ketel Marte",
        "3. Geraldo Perdomo",
        "4. Gabriel Moreno",
        "5. Adrian Del Castillo",
        "6. Nolan Arenado",
        "7. Carlos Santana",
        "8. Alek Thomas",
        "9. Tim Tawa"
    ],
    "bench": [
        "James McCann",
        "Jose Fernandez",
        "Ildemaro Vargas",
        "Jorge Barrosa"
    ],
    "rotation": [
        "1. Zac Gallen",
        "2. Ryne Nelson",
        "3. Eduardo Rodriguez",
        "4. Michael Soroka",
        "5. Brandon Pfaadt"
    ],
    "bullpen": [
        "CL - Paul Sewald",
        "SU - Jonathan Loáisiga",
        "SU - Juan Morillo",
        "MID - Taylor Clarke",
        "MID - Ryan Thompson",
        "MID - Andrew Hoffmann",
        "MID - Kevin Ginkel",
        "LR - Taylor Rashi"
    ],
    "injured": [
        "Corbin Burnes <br><span style='color: #8E8E93; font-size: 10px;'>60-Day IL • Tommy John • ETA: 2027</span>",
        "Merrill Kelly <br><span style='color: #8E8E93; font-size: 10px;'>15-Day IL • Nerve Irritation • ETA: Mid May</span>",
        "Jordan Lawlar <br><span style='color: #8E8E93; font-size: 10px;'>10-Day IL • Fractured Wrist • ETA: Late May</span>",
        "Pavin Smith <br><span style='color: #8E8E93; font-size: 10px;'>10-Day IL • Elbow • ETA: Late April</span>",
        "Lourdes Gurriel Jr. <br><span style='color: #8E8E93; font-size: 10px;'>10-Day IL • Torn ACL • ETA: Out for season</span>",
        "A.J. Puk <br><span style='color: #8E8E93; font-size: 10px;'>60-Day IL • Tommy John • ETA: 2027</span>",
        "Justin Martinez <br><span style='color: #8E8E93; font-size: 10px;'>60-Day IL • Tommy John • ETA: 2027</span>"
    ]
}

@st.cache_data(ttl=3600) 
def fetch_roster_resource():
    """Uses your backend depth chart, verifies active status with the MLB API."""
    url = "https://statsapi.mlb.com/api/v1/teams/109/roster?rosterType=active"
    
    try:
        res = requests.get(url, timeout=10).json()
        active_players = [item['person']['fullName'] for item in res.get('roster', [])]
        
        def verify_player(player_string):
            # Clean out the prefix numbers (e.g., "1. ") and roles (e.g., "CL - ") to match MLB API names
            clean_name = player_string.split(". ")[-1].split(" - ")[-1]
            if clean_name in active_players:
                return player_string
            else:
                return f"{player_string} <span style='color: #FF3B30; font-size: 10px;'>🔴 IL/MINORS</span>"
                
        return {
            "status": "Success",
            "lineup": [verify_player(p) for p in DEPTH_CHART["lineup"]],
            "bench": [verify_player(p) for p in DEPTH_CHART["bench"]],
            "rotation": [verify_player(p) for p in DEPTH_CHART["rotation"]],
            "bullpen": [verify_player(p) for p in DEPTH_CHART["bullpen"]],
            "injured": DEPTH_CHART["injured"] # IL guys don't need active verification
        }
        
    except Exception as e:
        return {
            "status": "Offline", "lineup": DEPTH_CHART["lineup"], "bench": DEPTH_CHART["bench"],
            "rotation": DEPTH_CHART["rotation"], "bullpen": DEPTH_CHART["bullpen"], "injured": DEPTH_CHART["injured"]
        }

# Run fetchers
live_slate = fetch_daily_slate()
roster_data = fetch_roster_resource()

# ==========================================
# 3. FRONTEND UI RENDERING
# ==========================================

# --- THE DAILY SLATE ---
az_tz = pytz.timezone('America/Phoenix')
display_date = datetime.now(az_tz).strftime("%B %d, %Y")
st.markdown(f'<div class="section-title">The Daily Slate ({display_date})</div>', unsafe_allow_html=True)
slate_cols = st.columns(5)

for col, team in zip(slate_cols, live_slate):
    with col:
        html_card = f'<div class="slick-card" style="text-align: center; padding: 15px;"><div class="sub-text">{team["name"]}</div><div style="font-size: 16px; font-weight: 800; margin: 8px 0;">{team["score"]}</div><div style="font-size: 12px; color: #8E8E93; font-weight: 500;">{team["hero"]}</div></div>'
        st.markdown(html_card, unsafe_allow_html=True)

# --- PLAYER SPOTLIGHT (Static placeholder for now) ---
st.markdown('<div class="section-title">Player Spotlight</div>', unsafe_allow_html=True)
spotlight_html = (
    '<div class="slick-card">'
    '<div style="display: flex; align-items: center; gap: 30px;">'
    '<div style="width: 100px; height: 100px; background-color: #E5E5EA; border-radius: 50%; display: flex; align-items: center; justify-content: center;"><span style="font-size: 30px;">📸</span></div>'
    '<div style="flex-grow: 1;">'
    '<div class="sub-text">STARTING PITCHER • TODAY</div>'
    '<div style="font-size: 24px; font-weight: 800; margin-bottom: 5px;">Zac Gallen</div>'
    '<div style="display: flex; gap: 20px;">'
    '<div><span class="sub-text">ERA</span> <span style="font-weight: 700;">3.60</span></div>'
    '<div><span class="sub-text">FIP</span> <span style="font-weight: 700;">3.40</span></div>'
    '</div></div></div></div>'
)
st.markdown(spotlight_html, unsafe_allow_html=True)

# --- THE MINI ROSTER RESOURCE (3-Column Layout) ---
col_hitters, col_pitchers, col_il = st.columns(3)

def build_roster_html(title, players, height="350px"):
    """Helper function to build scrollable list items with a built-in section header"""
    items = f'<div style="padding: 10px; background-color: #F9F9F9; border-bottom: 1px solid #E5E5EA; font-weight: 800; font-size: 14px; color: #1C1C1E;">{title}</div>'
    for player in players:
        items += f'<div style="padding: 10px; border-bottom: 1px solid #E5E5EA; font-size: 14px;">{player}</div>'
    return f'<div class="slick-card" style="padding: 0px; overflow: hidden;"><div class="scrollable-roster" style="max-height: {height};">{items}</div></div>'

with col_hitters:
    st.markdown('<div class="section-title">Position Players</div>', unsafe_allow_html=True)
    st.markdown(build_roster_html("Projected Lineup", roster_data['lineup'], "auto"), unsafe_allow_html=True)
    st.markdown(build_roster_html("Bench", roster_data['bench'], "auto"), unsafe_allow_html=True)

with col_pitchers:
    st.markdown('<div class="section-title">Pitching Staff</div>', unsafe_allow_html=True)
    st.markdown(build_roster_html("Starting Rotation", roster_data['rotation'], "auto"), unsafe_allow_html=True)
    st.markdown(build_roster_html("Bullpen", roster_data['bullpen'], "auto"), unsafe_allow_html=True)

with col_il:
    st.markdown('<div class="section-title">Recovery Tracker</div>', unsafe_allow_html=True)
    st.markdown(build_roster_html("Injured List", roster_data['injured'], "auto"), unsafe_allow_html=True)
# ==========================================
# 3. FRONTEND UI RENDERING
# ==========================================

# --- THE DAILY SLATE ---
az_tz = pytz.timezone('America/Phoenix')
display_date = datetime.now(az_tz).strftime("%B %d, %Y")
st.markdown(f'<div class="section-title">The Daily Slate ({display_date})</div>', unsafe_allow_html=True)
slate_cols = st.columns(5)

for col, team in zip(slate_cols, live_slate):
    with col:
        html_card = f'<div class="slick-card" style="text-align: center; padding: 15px;"><div class="sub-text">{team["name"]}</div><div style="font-size: 16px; font-weight: 800; margin: 8px 0;">{team["score"]}</div><div style="font-size: 12px; color: #8E8E93; font-weight: 500;">{team["hero"]}</div></div>'
        st.markdown(html_card, unsafe_allow_html=True)

# --- PLAYER SPOTLIGHT (Static for now until we hook up click events) ---
st.markdown('<div class="section-title">Player Spotlight</div>', unsafe_allow_html=True)
spotlight_html = (
    '<div class="slick-card">'
    '<div style="display: flex; align-items: center; gap: 30px;">'
    '<div style="width: 100px; height: 100px; background-color: #E5E5EA; border-radius: 50%; display: flex; align-items: center; justify-content: center;"><span style="font-size: 30px;">📸</span></div>'
    '<div style="flex-grow: 1;">'
    '<div class="sub-text">STARTING PITCHER • TODAY</div>'
    '<div style="font-size: 24px; font-weight: 800; margin-bottom: 5px;">Zac Gallen</div>'
    '<div style="display: flex; gap: 20px;">'
    '<div><span class="sub-text">ERA</span> <span style="font-weight: 700;">3.60</span></div>'
    '<div><span class="sub-text">FIP</span> <span style="font-weight: 700;">3.40</span></div>'
    '</div></div></div></div>'
)
st.markdown(spotlight_html, unsafe_allow_html=True)

# --- THE ACTIVE 26 (Scrollable Dynamic Cards) ---
col_lineup, col_rotation, col_bullpen = st.columns(3)

def build_roster_html(players):
    """Helper function to build scrollable list items"""
    items = ""
    for idx, player in enumerate(players):
        # Clean up FanGraphs weird characters if they exist
        clean_name = str(player).replace("(L)", "").replace("(S)", "").strip()
        items += f'<div style="padding: 10px; border-bottom: 1px solid #E5E5EA;"><b>{idx+1 if len(players) <= 9 else ""}. {clean_name}</b></div>'
    return f'<div class="slick-card" style="padding: 0px;"><div class="scrollable-roster">{items}</div></div>'

with col_lineup:
    st.markdown('<div class="section-title">Projected Lineup</div>', unsafe_allow_html=True)
    st.markdown(build_roster_html(roster_data['lineup']), unsafe_allow_html=True)

with col_rotation:
    st.markdown('<div class="section-title">The Rotation</div>', unsafe_allow_html=True)
    st.markdown(build_roster_html(roster_data['rotation']), unsafe_allow_html=True)

with col_bullpen:
    st.markdown('<div class="section-title">The Bullpen</div>', unsafe_allow_html=True)
    st.markdown(build_roster_html(roster_data['bullpen']), unsafe_allow_html=True)
