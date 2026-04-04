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
        background-color: #FFFFFF; border-radius: 0 0 12px 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04); border: none;
    }
    
    div[data-baseweb="tab-list"] { background-color: #E5E5EA; border-radius: 10px; padding: 4px; gap: 4px; }
    button[data-baseweb="tab"] { background-color: transparent !important; border-radius: 8px !important; color: #1C1C1E !important; font-weight: 600 !important; padding: 8px 16px !important; border: none !important; }
    button[data-baseweb="tab"][aria-selected="true"] { background-color: #FFFFFF !important; box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important; }

    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("🐍 Databacks")
    page = st.radio("Menu", ["Live Game", "The Lab", "Farm System", "Articles"])
    st.caption("UI Prototype v8.0 - Pitch Usage & BB%")

# 4. MAIN ROUTING LOGIC
if page == "Live Game":
    
    st.markdown("<h2 style='color: #1C1C1E; font-weight: 400; margin-bottom: 0px;'>Braves vs. Dbacks - 4/3/2026</h2>", unsafe_allow_html=True)
    st.write("") 
    
    tab1, tab2, tab3 = st.tabs(["Live AB", "Scoreboard", "Box Score"])
    
    with tab1:
        st.write("") 
        
        # --- TOP ROW: MATCHUP (Custom HTML Grids) ---
        top_col1, top_col2 = st.columns(2)
        
        with top_col1:
            st.markdown("""
            <div style="background-color: #13274F; color: white; padding: 10px 15px; border-radius: 12px 12px 0 0; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">AT THE PLATE</div>
            <div style="background-color: white; border-radius: 0 0 12px 12px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); display: grid; grid-template-columns: 2.2fr 0.8fr 0.8fr 0.8fr 0.8fr 1.2fr 1.2fr 1fr; text-align: center; align-items: center;">
                <div style="text-align: left;">
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">BATTER</div>
                    <div style="font-size: 15px; font-weight: 800; color: #13274F;">Drake Baldwin</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-top: 4px;">Season</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">AB</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">2</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-top: 4px;">.284</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">H</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">0</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-top: 4px;">61</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">BB</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">1</div>
                    <div style="font-size: 13px; font-weight: 800; color: #1C1C1E; background-color: #E5E5EA; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">11.2%</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">K</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">1</div>
                    <div style="font-size: 13px; font-weight: 800; color: #1C1C1E; background-color: #F1A7AA; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">16.5%</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">AVG EV</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">105.0</div>
                    <div style="font-size: 13px; font-weight: 800; color: white; background-color: #D22D49; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">91.2</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">HARD HITS</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">1</div>
                    <div style="font-size: 13px; font-weight: 800; color: #1C1C1E; background-color: #F1A7AA; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">42.1%</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">WHIFFS</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">0</div>
                    <div style="font-size: 13px; font-weight: 800; color: white; background-color: #D22D49; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">14.5%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with top_col2:
            st.markdown("""
            <div style="background-color: #A71930; color: white; padding: 10px 15px; border-radius: 12px 12px 0 0; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">ON THE MOUND</div>
            <div style="background-color: white; border-radius: 0 0 12px 12px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); display: grid; grid-template-columns: 2.2fr 1fr 1fr 1fr 1.2fr 1fr; text-align: center; align-items: center;">
                <div style="text-align: left;">
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">PITCHER</div>
                    <div style="font-size: 15px; font-weight: 800; color: #A71930;">Eduardo Rodriguez</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-top: 4px;">Season</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">IP</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">5.1</div>
                    <div style="font-size: 13px; font-weight: 700; color: #8E8E93; margin-top: 4px;">114.0</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">K</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">4</div>
                    <div style="font-size: 13px; font-weight: 800; color: #1C1C1E; background-color: #F1A7AA; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">24.5%</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">BB</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">2</div>
                    <div style="font-size: 13px; font-weight: 800; color: #1C1C1E; background-color: #E5E5EA; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">7.8%</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">WHIFFS</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">6</div>
                    <div style="font-size: 13px; font-weight: 800; color: #1C1C1E; background-color: #F1A7AA; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">28.5%</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #8E8E93; font-weight: 700; margin-bottom: 4px;">STUFF+</div>
                    <div style="font-size: 15px; font-weight: 800; color: #1C1C1E;">96</div>
                    <div style="font-size: 13px; font-weight: 800; color: #1C1C1E; background-color: #E5E5EA; border-radius: 4px; padding: 2px 4px; display: inline-block; margin-top: 2px;">98</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.write("")

        # --- BOTTOM ROW: LIVE SITUATION (3 Columns) ---
        bot_col1, bot_col2, bot_col3 = st.columns([1.2, 0.8, 1.2])

        # LEFT: SCOREBUG
        with bot_col1:
            st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px;">Game Situation</div>', unsafe_allow_html=True)
            components.html("""
            <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
                <div style="background: white; border-radius: 16px; padding: 15px 25px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #E5E5EA; height: 90px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);">
                    <div style="display: flex; gap: 20px; align-items: center;">
                        <div style="text-align: center;">
                            <div style="font-size: 16px; font-weight: 800; color: #1C1C1E;">ATL</div>
                            <div style="font-size: 20px; font-weight: 600; color: #8E8E93;">2</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 16px; font-weight: 800; color: #A71930;">AZ</div>
                            <div style="font-size: 20px; font-weight: 600; color: #8E8E93;">0</div>
                        </div>
                    </div>
                    <div style="font-size: 20px; font-weight: 800; color: #1C1C1E; border-left: 1px solid #E5E5EA; border-right: 1px solid #E5E5EA; padding: 0 25px;">
                        ▲ 6th
                    </div>
                    <div style="display: flex; justify-content: flex-end; align-items: center; gap: 15px;">
                        <div style="text-align: right;">
                            <div style="font-size: 18px; font-weight: 800; color: #1C1C1E;">1 - 1</div>
                            <div style="font-size: 13px; font-weight: 600; color: #8E8E93; margin-top: 2px;">1 Out</div>
                        </div>
                        <div style="position: relative; width: 36px; height: 36px;">
                            <div style="position: absolute; top: 4px; left: 13px; width: 10px; height: 10px; transform: rotate(45deg); border: 2px solid #C7C7CC;"></div>
                            <div style="position: absolute; top: 16px; left: 0px; width: 10px; height: 10px; transform: rotate(45deg); border: 2px solid #C7C7CC;"></div>
                            <div style="position: absolute; top: 16px; left: 26px; width: 10px; height: 10px; transform: rotate(45deg); background-color: #13274F; border: 2px solid #13274F;"></div>
                        </div>
                    </div>
                </div>
                <div style="text-align: right; margin-top: 8px; font-size: 13px; font-weight: 700; color: #8E8E93; padding-right: 5px;">
                    <span style="color: #A71930;">Rodriguez</span> P: 72
                </div>
            </div>
            """, height=135)

        # CENTER: 2D STRIKE ZONE
        with bot_col2:
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

            ax.scatter(0.3, 0.8, color='#FF8200', s=200, zorder=5, edgecolor='white', linewidth=1.5)
            ax.text(0.3, 0.8, '1', color='white', fontsize=9, ha='center', va='center', weight='bold', zorder=6)
            
            ax.scatter(-0.5, 1.8, color='#00D1ED', s=200, zorder=5, edgecolor='white', linewidth=1.5)
            ax.text(-0.5, 1.8, '2', color='white', fontsize=9, ha='center', va='center', weight='bold', zorder=6)

            ax.scatter(0.1, 2.6, color='#933F2C', s=200, zorder=5, edgecolor='white', linewidth=1.5)
            ax.text(0.1, 2.6, '3', color='white', fontsize=9, ha='center', va='center', weight='bold', zorder=6)

            ax.axis('off')
            st.pyplot(fig, transparent=True)

        # RIGHT: PITCH USAGE & SEQUENCE 
        with bot_col3:
            st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px;">Pitch Usage</div>', unsafe_allow_html=True)
            
            # Custom HTML Grid for Pitch Usage
            st.markdown("""
            <div style="background-color: white; border-radius: 12px; padding: 12px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); display: flex; justify-content: space-between; text-align: center; border: 1px solid #E5E5EA; margin-bottom: 20px;">
                <div style="text-align: left; display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 13px; font-weight: 800; color: #1C1C1E;">Game</div>
                    <div style="font-size: 12px; font-weight: 700; color: #8E8E93; margin-top: 4px;">Season</div>
                </div>
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: #FF8200;">SI</div>
                    <div style="font-size: 14px; font-weight: 800; color: #1C1C1E; margin-top: 2px;">44%</div>
                    <div style="font-size: 12px; font-weight: 700; color: #8E8E93; margin-top: 2px;">41%</div>
                </div>
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: #933F2C;">FC</div>
                    <div style="font-size: 14px; font-weight: 800; color: #1C1C1E; margin-top: 2px;">26%</div>
                    <div style="font-size: 12px; font-weight: 700; color: #8E8E93; margin-top: 2px;">22%</div>
                </div>
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: #00D1ED;">CU</div>
                    <div style="font-size: 14px; font-weight: 800; color: #1C1C1E; margin-top: 2px;">18%</div>
                    <div style="font-size: 12px; font-weight: 700; color: #8E8E93; margin-top: 2px;">15%</div>
                </div>
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: #D22D49;">FF</div>
                    <div style="font-size: 14px; font-weight: 800; color: #1C1C1E; margin-top: 2px;">12%</div>
                    <div style="font-size: 12px; font-weight: 700; color: #8E8E93; margin-top: 2px;">22%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div style="font-weight: 700; font-size: 16px; color: #1C1C1E; margin-bottom: 5px;">Pitch Sequence</div>', unsafe_allow_html=True)
            
            pitch_seq = pd.DataFrame({
                "#": [1, 2, 3],
                "Pitch": ["SI", "CU", "FC"],
                "Result": ["Ball In Dirt", "Called Strike", "In play, out(s)"],
                "Vel": [86.9, 78.3, 86.6],
                "Spin": [2206, 2225, 2203],
                "IVB": [6, -5, 8],
                "HB": [1, 5, 2],
                "Stuff+": [92, 108, 98]
            })

            def color_pitches(val):
                colors = {'SI': '#FF8200', 'CU': '#00D1ED', 'FC': '#933F2C', 'FF': '#D22D49', 'CH': '#1DBE3A', 'SL': '#E3E1A6'}
                color = colors.get(val, '#1C1C1E')
                return f'color: {color}; font-weight: 800;'

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
