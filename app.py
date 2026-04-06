import streamlit as st
import pandas as pd
import cloudscraper # NEW: Replaces 'requests' to bypass FanGraphs security
import requests
from datetime import datetime
import pytz # NEW: For accurate timezones

# ... [KEEP YOUR EXISTING PAGE SETUP & UI CSS HERE] ...

# ==========================================
# 2. BACKEND DATA ENGINES
# ==========================================

@st.cache_data(ttl=300) 
def fetch_daily_slate():
    """Fetches live schedule/scores from MLB Stats API for the D-backs system."""
    # Force Arizona timezone so the server UTC clock doesn't grab the wrong day
    az_tz = pytz.timezone('America/Phoenix')
    today = datetime.now(az_tz).strftime('%Y-%m-%d')
    
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
                    # Grab game time and convert formatting
                    game_time = game['gameDate'].split('T')[1][:5]
                    score_text = f"{game_time} UTC"
                    hero_text = "Scheduled"
                else:
                    away_score = game['teams']['away'].get('score', 0)
                    home_score = game['teams']['home'].get('score', 0)
                    score_text = f"{away_score} - {home_score} ({status})"
                    hero_text = "Live Data Loaded"
                
                slate.append({"name": name, "score": score_text, "hero": hero_text})
            else:
                slate.append({"name": name, "score": "OFF", "hero": "No game today"})
        except Exception as e:
            slate.append({"name": name, "score": "Error", "hero": "API Failed"})
            
    return slate

@st.cache_data(ttl=3600) 
def fetch_roster_resource():
    """Scrapes FanGraphs D-Backs Depth Chart using Cloudscraper."""
    url = "https://www.fangraphs.com/roster-resource/depth-charts/diamondbacks"
    
    try:
        # Create a scraper to bypass Cloudflare
        scraper = cloudscraper.create_scraper()
        html = scraper.get(url).text
        
        # Read the raw HTML into pandas
        dfs = pd.read_html(html)
        
        return {
            "status": "Success",
            "lineup": dfs[0]['Player'].dropna().tolist()[:9] if len(dfs) > 0 else ["Lineup Not Found"],
            "rotation": dfs[1]['Player'].dropna().tolist()[:5] if len(dfs) > 1 else ["Rotation Not Found"],
            "bullpen": dfs[2]['Player'].dropna().tolist()[:8] if len(dfs) > 2 else ["Bullpen Not Found"]
        }
    except Exception as e:
        return {"status": "Failed", "lineup": [f"Scrape Error: {e}"], "rotation": ["Error"], "bullpen": ["Error"]}

# Run fetchers
live_slate = fetch_daily_slate()
roster_data = fetch_roster_resource()

# ... [KEEP YOUR EXISTING FRONTEND UI RENDERING HERE] ...
