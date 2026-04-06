import streamlit as st

# 1. PAGE SETUP & SLICK UI CSS
st.set_page_config(page_title="Databacks | Home", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp { background-color: #F2F2F7; color: #1C1C1E; font-family: -apple-system, sans-serif; }
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

.slick-card { 
    background-color: #FFFFFF; border-radius: 16px; padding: 20px; 
    box-shadow: 0 4px 16px rgba(0,0,0,0.05); border: 1px solid #E5E5EA; margin-bottom: 16px; 
}
.section-title { font-size: 18px; font-weight: 800; color: #1C1C1E; margin-bottom: 12px; }
.sub-text { font-size: 12px; font-weight: 600; color: #8E8E93; text-transform: uppercase; }
.big-stat { font-size: 28px; font-weight: 900; color: #1C1C1E; }

.bar-bg { background-color: #E5E5EA; border-radius: 8px; height: 8px; width: 100%; margin-top: 4px; }
.bar-red { background-color: #D22D49; border-radius: 8px; height: 100%; }
.bar-blue { background-color: #3B71CA; border-radius: 8px; height: 100%; }
</style>
""", unsafe_allow_html=True)

# 2. THE DAILY SLATE (Top Row)
st.markdown('<div class="section-title">The Daily Slate (April 6, 2026)</div>', unsafe_allow_html=True)

slate_cols = st.columns(5)
teams = [
    {"name": "D-Backs", "score": "vs. NYM - 4:10 PM", "hero": "Gallen Starting"},
    {"name": "Aces (AAA)", "score": "L 3-4", "hero": "Lawlar: 1-3, BB"},
    {"name": "Sod Poodles (AA)", "score": "7:05 PM", "hero": "Lin starting"},
    {"name": "Hops (A+)", "score": "W 8-1", "hero": "Melendez: 3-5, 2B"},
    {"name": "Rawhide (A)", "score": "6:30 PM", "hero": "TBA"}
]

for col, team in zip(slate_cols, teams):
    with col:
        # Single-line string to avoid markdown parsing bugs
        html_card = f'<div class="slick-card" style="text-align: center; padding: 15px;"><div class="sub-text">{team["name"]}</div><div style="font-size: 20px; font-weight: 800; margin: 8px 0;">{team["score"]}</div><div style="font-size: 12px; color: #8E8E93; font-weight: 500;">{team["hero"]}</div></div>'
        st.markdown(html_card, unsafe_allow_html=True)

# 3. ANCHORED PLAYER SPOTLIGHT (Middle Row)
st.markdown('<div class="section-title">Player Spotlight</div>', unsafe_allow_html=True)

# Wrapped in parentheses to concatenate safely without linebreaks messing up Streamlit
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
    '<div><span class="sub-text">WHIP</span> <span style="font-weight: 700;">1.10</span></div>'
    '</div></div>'
    '<div style="min-width: 250px;">'
    '<div style="margin-bottom: 10px;"><div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 700;"><span>K%</span> <span style="color: #D22D49;">85th</span></div><div class="bar-bg"><div class="bar-red" style="width: 85%;"></div></div></div>'
    '<div style="margin-bottom: 10px;"><div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 700;"><span>Whiff%</span> <span style="color: #D22D49;">72nd</span></div><div class="bar-bg"><div class="bar-red" style="width: 72%;"></div></div></div>'
    '<div><div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 700;"><span>Avg EV</span> <span style="color: #3B71CA;">30th</span></div><div class="bar-bg"><div class="bar-blue" style="width: 30%;"></div></div></div>'
    '</div></div></div>'
)
st.markdown(spotlight_html, unsafe_allow_html=True)

# 4. THE ACTIVE 26 (Bottom Row - UPDATED 2026 ROSTER)
col_lineup, col_rotation, col_bullpen = st.columns(3)

with col_lineup:
    st.markdown('<div class="section-title">Projected Lineup</div>', unsafe_allow_html=True)
    lineup_html = (
        '<div class="slick-card" style="padding: 10px;">'
        '<div style="padding: 8px; border-bottom: 1px solid #E5E5EA; display: flex; justify-content: space-between;"><b>1. Ketel Marte</b> <span style="color: #8E8E93;">S</span></div>'
        '<div style="padding: 8px; border-bottom: 1px solid #E5E5EA; display: flex; justify-content: space-between;"><b>2. Corbin Carroll</b> <span style="color: #8E8E93;">L</span></div>'
        '<div style="padding: 8px; border-bottom: 1px solid #E5E5EA; display: flex; justify-content: space-between;"><b>3. Geraldo Perdomo</b> <span style="color: #8E8E93;">S</span></div>'
        '<div style="padding: 8px; border-bottom: 1px solid #E5E5EA; display: flex; justify-content: space-between;"><b>4. Nolan Arenado</b> <span style="color: #8E8E93;">R</span></div>'
        '<div style="padding: 8px; border-bottom: 1px solid #E5E5EA; display: flex; justify-content: space-between;"><b>5. Gabriel Moreno</b> <span style="color: #8E8E93;">R</span></div>'
        '<div style="padding: 8px; border-bottom: 1px solid #E5E5EA; display: flex; justify-content: space-between;"><b>6. Carlos Santana</b> <span style="color: #8E8E93;">S</span></div>'
        '<div style="padding: 8px; color: #8E8E93; font-size: 12px; text-align: center;">View Full 9...</div>'
        '</div>'
    )
    st.markdown(lineup_html, unsafe_allow_html=True)

with col_rotation:
    st.markdown('<div class="section-title">The Rotation</div>', unsafe_allow_html=True)
    rotation_html = (
        '<div class="slick-card" style="padding: 10px;">'
        '<div style="padding: 8px; border-bottom: 1px solid #E5E5EA; background-color: #F9F9F9; border-left: 4px solid #A71930;"><b>Zac Gallen</b> <span style="font-size: 11px; float: right; color: #A71930; font-weight: bold;">TODAY</span></div>'
        '<div style="padding: 8px; border-bottom: 1px solid #E5E5EA;"><b>Brandon Pfaadt</b></div>'
        '<div style="padding: 8px; border-bottom: 1px solid #E5E5EA;"><b>Eduardo Rodriguez</b></div>'
        '<div style="padding: 8px; border-bottom: 1px solid #E5E5EA;"><b>Ryne Nelson</b></div>'
        '<div style="padding: 8px;"><b>Michael Soroka</b></div>'
        '</div>'
    )
    st.markdown(rotation_html, unsafe_allow_html=True)

with col_bullpen:
    st.markdown('<div class="section-title">The Bullpen</div>', unsafe_allow_html=True)
    bullpen_html = (
        '<div class="slick-card" style="padding: 10px;">'
        '<div style="padding: 8px; border-bottom: 1px solid #E5E5EA; display: flex; justify-content: space-between;"><b>Paul Sewald</b> <span style="color: #34C759; font-size: 12px; font-weight: bold;">RESTED</span></div>'
        '<div style="padding: 8px; border-bottom: 1px solid #E5E5EA; display: flex; justify-content: space-between;"><b>Kevin Ginkel</b> <span style="color: #FF3B30; font-size: 12px; font-weight: bold;">20 P</span></div>'
        '<div style="padding: 8px; border-bottom: 1px solid #E5E5EA; display: flex; justify-content: space-between;"><b>Ryan Thompson</b> <span style="color: #34C759; font-size: 12px; font-weight: bold;">RESTED</span></div>'
        '<div style="padding: 8px; border-bottom: 1px solid #E5E5EA; display: flex; justify-content: space-between;"><b>Jonathan Loáisiga</b> <span style="color: #34C759; font-size: 12px; font-weight: bold;">RESTED</span></div>'
        '<div style="padding: 8px; color: #8E8E93; font-size: 12px; text-align: center;">View All...</div>'
        '</div>'
    )
    st.markdown(bullpen_html, unsafe_allow_html=True)
