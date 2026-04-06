import streamlit as st
import pandas as pd
import requests
from datetime import datetime

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
# 2. BACKEND DATA ENGINES
# ==========================================

@st.cache_data(ttl=300) # Refreshes every 5 minutes
def fetch_daily_slate():
    """Fetches live schedule/scores from MLB Stats API for the D-backs system."""
    today = datetime.today().strftime('%Y-%m-%d')
    # IDs: 109 (AZ), 238 (Reno), 3251 (Amarillo), 425 (Hillsboro), 430 (Visalia)
    team_ids = {"D-Backs": 109, "Aces (AAA)": 238, "Sod Poodles (AA)": 3251, "Hops (A+)": 425, "Rawhide (A)": 430}
    slate = []
    
    for name, team_id in team_ids.items():
        try:
            url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1,11,12,13,14&teamId={team_id}&date={today}&hydrate=probablePitcher(note)"
            res = requests.get(url).json()
            
            if res['totalItems'] > 0:
                game = res['dates'][0]['games'][0]
                status = game['status']['detailedState']
                
                if status == "Scheduled" or status == "Pre-Game":
                    time = game['gameDate'].split('T')[1][:5] # Rough UTC time extraction
                    score_text = f"{time} UTC"
                else:
                    away_score = game['teams']['away'].get('score', 0)
                    home_score = game['teams']['home'].get('score', 0)
                    score_text = f"{away_score} - {home_score} ({status})"
                
                slate.append({"name": name, "score": score_text, "hero": "Live Data Loaded"})
            else:
                slate.append({"name": name, "score": "OFF", "hero": "No game today"})
        except Exception as e:
            slate.append({"name": name, "score": "Error", "hero": "Check API"})
            
    return slate

@st.cache_data(ttl=3600) # Refreshes every 1 hour
def fetch_roster_resource():
    """Scrapes FanGraphs D-Backs Depth Chart."""
    url = "https://www.fangraphs.com/roster-resource/depth-charts/diamondbacks"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    try:
        html = requests.get(url, headers=headers).text
        dfs = pd.read_html(html)
        # FanGraphs usually puts the Starting Lineup in the first table, Rotation/Bullpen further down.
        # This is a safe fallback list if FanGraphs blocks us.
        return {
            "status": "Success",
            "lineup": dfs[0]['Player'].dropna().tolist()[:9] if len(dfs) > 0 else ["Lineup Not Found"],
            "rotation": dfs[1]['Player'].dropna().tolist()[:5] if len(dfs) > 1 else ["Rotation Not Found"],
            "bullpen": dfs[2]['Player'].dropna().tolist()[:8] if len(dfs) > 2 else ["Bullpen Not Found"]
        }
    except Exception as e:
        return {"status": "Failed", "lineup": ["Error scraping FanGraphs"], "rotation": ["Error"], "bullpen": ["Error"]}

# Run fetchers
live_slate = fetch_daily_slate()
roster_data = fetch_roster_resource()

# ==========================================
# 3. FRONTEND UI RENDERING
# ==========================================

# --- THE DAILY SLATE ---
st.markdown(f'<div class="section-title">The Daily Slate ({datetime.today().strftime("%B %d, %Y")})</div>', unsafe_allow_html=True)
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
