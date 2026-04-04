import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 1. PAGE SETUP
st.set_page_config(page_title="Databacks", page_icon="🐍", layout="wide", initial_sidebar_state="expanded")

# 2. APPLE HEALTH & SAVANT HYBRID CSS
st.markdown("""
<style>
    .stApp { background-color: #F2F2F7; color: #1C1C1E; }
    
    div[data-testid="stDataFrame"] > div {
        background-color: #FFFFFF;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        border: none;
    }
    
    div[data-baseweb="tab-list"] { background-color: #E5E5EA; border-radius: 10px; padding: 4px; gap: 4px; }
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 8px !important;
        color: #1C1C1E !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        border: none !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #FFFFFF !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("🐍 Databacks")
    page = st.radio("Menu", ["Live Game", "The Lab", "Farm System", "Articles"])
    st.caption("UI Prototype v5.1 - Polished Scorebug & Colors")

# 4. MAIN ROUTING LOGIC
if page == "Live Game":
    
    st.markdown("<h2 style='color: #1C1C1E; font-weight: 400; margin-bottom: 0px;'>Braves vs. Dbacks - 4/3/2026</h2>", unsafe_allow_html=True)
    st.write("") 
    
    tab1, tab2, tab3 = st.tabs(["Live AB", "Scoreboard", "Box Score"])
    
    with tab1:
        st.write("") 
        
        # --- TOP ROW: MATCHUP (2 Columns) ---
        top_col1, top_col2 = st.columns(2)
        
        with top_col1:
            st.markdown('<div style="background-color: #13274F; color: white; padding: 10px 15px; border-radius: 12px 12px 0 0; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">AT THE PLATE</div>', unsafe_allow_html=True)
            # Season Context Text
            st.markdown('<div style="background-color: white; color: #8E8E93; font-size: 13px; font-weight: 700; padding: 8px 15px 0px 15px;">2026 Season: .284 AVG • .820 OPS • 14.5% Whiff%</div>', unsafe_allow_html=True)
            
            batter_data = pd.DataFrame({
                "Batter": ["Drake Baldwin"], "AB": [2], "H": [0], 
                "Avg EV": [105.0], "Hard Hits": [1], "Whiff %": [0.0]
            })
            
            # Format Batter Table (Blue for High Whiff% for batter)
            styled_batter = batter_data.style.background_gradient(
                subset=['Whiff %'], cmap='coolwarm', vmin=15, vmax=35
            ).format({"Whiff %": "{:.1f}%", "Avg EV": "{:.1f}"})
            
            st.dataframe(styled_batter, hide_index=True, use_container_width=True)
            
        with top_col2:
            st.markdown('<div style="background-color: #A71930; color: white; padding: 10px 15px; border-radius: 12px 12px 0 0; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">ON THE MOUND</div>', unsafe_allow_html=True)
            # Season Context Text
            st.markdown('<div style="background-color: white; color: #8E8E93; font-size: 13px; font-weight: 700; padding: 8px 15px 0px 15px;">2026 Season: 3.42 ERA • 1.12 WHIP • 28.5% Whiff%</div>', unsafe_allow_html=True)
            
            pitcher_data = pd.DataFrame({
                "Pitcher": ["Eduardo Rodriguez"], "IP": ["5.1"], "K": [4], 
                "Pitches": [72], "Whiff %": [18.5], "Stuff+": [96] 
            })

            # Format Pitcher Table (Red for High Stuff+ / High Whiff%)
            styled_pitcher = pitcher_data.style.background_gradient(
                subset=['Stuff+'], cmap='coolwarm', vmin=70, vmax=130
            ).background_gradient(
                subset=['Whiff %'], cmap='coolwarm', vmin=15, vmax=35
            ).format({"Whiff %": "{:.1f}%", "Stuff+": "{:.0f}"})

            st.dataframe(styled_pitcher, hide_index=True, use_container_width=True)

        st.write("")
        st.write("")

        # --- BOTTOM ROW: LIVE SITUATION (3 Columns) ---
        bot_col1, bot_col2, bot_col3 = st.columns([1.2, 0.8, 1.2])

        # LEFT: SCOREBUG (Redesigned Flexbox)
        with bot_col1:
            st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px;">Game Situation</div>', unsafe_allow_html=True)
            components.html("""
            <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: white; border-radius: 16px; padding: 15px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); display: flex; justify-content: space-between; align-items: center; border: 1px solid #E5E5EA; height: 100%; min-height: 85px;">
                
                <div style="display: flex; gap: 20px; align-items: center; flex: 1;">
                    <div style="display: flex; gap: 15px; align-items: center;">
                        <div style="text-align: center;">
                            <div style="font-size: 18px; font-weight: 800; color: #1C1C1E;">ATL</div>
                            <div style="font-size: 20px; font-weight: 600; color: #8E8E93;">2</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 18px; font-weight: 800; color: #A71930;">AZ</div>
                            <div style="font-size: 20px; font-weight: 600; color: #8E8E93;">0</div>
                        </div>
                    </div>
                    <div style="font-size: 22px; font-weight: 800; color: #1C1C1E; margin-left: 10px;">▲ 6th</div>
                </div>

                <div style="display: flex; gap: 15px; align-items: center; justify-content: center; flex: 1; border-left: 1px solid #E5E5EA; border-right: 1px solid #E5E5EA; padding: 0 15px;">
                    <div style="text-align: right;">
                        <div style="font-size: 20px; font-weight: 800; color: #1C1C1E;">1 - 1</div>
                        <div style="font-size: 14px; font-weight: 600; color: #8E8E93; margin-top: 2px;">1 Out</div>
                    </div>
                    <div style="position: relative; width: 40px; height: 40px; margin-left: 5px;">
                        <div style="position: absolute; top: 4px; left: 14px; width: 12px; height: 12px; transform: rotate(45deg); border: 2px solid #C7C7CC;"></div>
                        <div style="position: absolute; top: 18px; left: 0px; width: 12px; height: 12px; transform: rotate(45deg); border: 2px solid #C7C7CC;"></div>
                        <div style="position: absolute; top: 18px; left: 28px; width: 12px; height: 12px; transform: rotate(45deg); background-color: #13274F; border: 2px solid #13274F;"></div>
                    </div>
                </div>

                <div style="text-align: right; flex: 1;">
                    <div style="font-size: 12px; font-weight: 700; color: #8E8E93; text-transform: uppercase; letter-spacing: 0.5px;">Win Prob</div>
                    <div style="font-size: 24px; font-weight: 800; color: #1C1C1E; margin-top: 2px;">ATL 74.2%</div>
                </div>

            </div>
            """, height=120)

        # CENTER: 2D STRIKE ZONE (Solid Lines)
        with bot_col2:
            st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px; text-align: center;">Pitch Location</div>', unsafe_allow_html=True)
            
            fig, ax = plt.subplots(figsize=(3, 3))
            fig.patch.set_facecolor('#F2F2F7') 
            ax.set_facecolor('#F2F2F7')
            
            ax.set_xlim(-2, 2)
            ax.set_ylim(0, 5)

            # Draw Home Plate
            plate = patches.Polygon([(-0.71, 0.1), (0.71, 0.1), (0.71, 0.3), (0, 0.5), (-0.71, 0.3)], closed=True, facecolor='#E5E5EA', edgecolor='#C7C7CC')
            ax.add_patch(plate)

            # Draw Strike Zone (Solid Line via linestyle='-')
            zone = patches.Rectangle((-0.71, 1.5), 1.42, 2.0, linewidth=2, edgecolor='#8E8E93', facecolor='none', linestyle='-')
            ax.add_patch(zone)

            # Plot Pitches
            ax.scatter(0.3, 0.8, color='#FF8200', s=200, zorder=5, edgecolor='white', linewidth=1.5)
            ax.text(0.3, 0.8, '1', color='white', fontsize=9, ha='center', va='center', weight='bold', zorder=6)
            
            ax.scatter(-0.5, 1.8, color='#00D1ED', s=200, zorder=5, edgecolor='white', linewidth=1.5)
            ax.text(-0.5, 1.8, '2', color='white', fontsize=9, ha='center', va='center', weight='bold', zorder=6)

            ax.scatter(0.1, 2.6, color='#933F2C', s=200, zorder=5, edgecolor='white', linewidth=1.5)
            ax.text(0.1, 2.6, '3', color='white', fontsize=9, ha='center', va='center', weight='bold', zorder=6)

            ax.axis('off')
            st.pyplot(fig, transparent=True)

        # RIGHT: PITCH SEQUENCE (Gradient Colors & Decimal Velo)
        with bot_col3:
            st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px;">Pitch Sequence</div>', unsafe_allow_html=True)
            
            pitch_seq = pd.DataFrame({
                "#": [1, 2, 3],
                "Pitch": ["Sinker", "Curveball", "Cutter"],
                "Result": ["Ball In Dirt", "Called Strike", "In play, out(s)"],
                "Vel": [86.9, 78.3, 86.6],
                "Spin": [2206, 2225, 2203],
                "IVB": [6, -5, 8],
                "HB": [1, 5, 2],
                "Stuff+": [92, 108, 98]
            })

            def color_pitches(val):
                colors = {'Sinker': '#FF8200', 'Curveball': '#00D1ED', 'Cutter': '#933F2C'}
                color = colors.get(val, '#1C1C1E')
                return f'color: {color}; font-weight: 700;'

            # Map the text colors, then apply the Savant red/blue gradient to Stuff+, then format decimals
            styled_seq = pitch_seq.style.map(color_pitches, subset=['Pitch']) \
                .background_gradient(subset=['Stuff+'], cmap='coolwarm', vmin=70, vmax=130) \
                .format({"Vel": "{:.1f}", "Stuff+": "{:.0f}"})

            st.dataframe(
                styled_seq, 
                hide_index=True, 
                use_container_width=True,
                column_config={"#": st.column_config.NumberColumn(width="small")}
            )

    with tab2:
        st.info("Scoreboard components will load here.")
    with tab3:
        st.info("Box score table will load here.")

else:
    st.title(page)
    st.markdown(f"*{page} module is currently under construction. Check back soon.*")
