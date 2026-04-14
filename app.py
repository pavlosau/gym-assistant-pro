import streamlit as st
import datetime
import pandas as pd
import numpy as np

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="Hybrid Nexus AI", layout="centered", page_icon="⚡")

# Business Logic: Gym Partner Database
gym_configs = {
    "Individual Subscriber": {"color": "#FF4B4B", "logo": "👤", "tagline": "Personal Elite Performance"},
    "Iron Paradise Gym": {"color": "#1E90FF", "logo": "🏋️‍♂️", "tagline": "Strength & Grit Facility"},
    "Elite Endurance Hub": {"color": "#32CD32", "logo": "🏃‍♂️", "tagline": "The Home of Hybrid Athletes"},
    "Metabolic CrossFit": {"color": "#FFD700", "logo": "🔥", "tagline": "Forge Your Fitness"}
}

# Sidebar Styling & Logo Selection
st.sidebar.header("🏢 Partner Portal")
selected_gym = st.sidebar.selectbox("Current Location", list(gym_configs.keys()))
theme_color = gym_configs[selected_gym]["color"]
gym_logo = gym_configs[selected_gym]["logo"]
tagline = gym_configs[selected_gym]["tagline"]

# Professional UI Injection
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: white; }}
    .stButton>button {{ 
        width: 100%; border-radius: 8px; 
        background-color: {theme_color}; color: white; border: none;
        font-weight: bold; height: 3.5em; transition: 0.3s;
    }}
    .stButton>button:hover {{ opacity: 0.8; border: 1px solid white; }}
    .stProgress > div > div > div > div {{ background-color: {theme_color}; }}
    [data-testid="stMetricValue"] {{ color: {theme_color}; font-family: 'Courier New'; }}
    div.stBlock {{ border: 1px solid #333; padding: 20px; border-radius: 10px; background: #161b22; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. ATHLETE ONBOARDING (Sidebar) ---
st.sidebar.divider()
st.sidebar.header("👤 Athlete Bio")
u_name = st.sidebar.text_input("Name", "Alex")
u_weight = st.sidebar.number_input("Current Weight (kg)", 40, 200, 85)
u_goal = st.sidebar.selectbox("Season Goal", ["Hyrox Pro", "Hyrox Open", "Marathon Prep", "Half-Marathon"])
u_level = st.sidebar.select_slider("Experience Level", options=["Beginner", "Intermediate", "Advanced", "Elite"])

# Calculating Training Phases
# This simulates a 'Periodization' engine
weeks_to_race = st.sidebar.slider("Weeks until Race", 1, 20, 12)
if weeks_to_race > 8: phase = "Base Building"
elif weeks_to_race > 4: phase = "Peak Intensity"
else: phase = "Tapering / Recovery"

# --- 3. MAIN DASHBOARD ---
st.title(f"{gym_logo} {selected_gym}")
st.caption(f"_{tagline}_")

# Summary Metrics Row
m1, m2, m3 = st.columns(3)
m1.metric("Current Phase", phase)
m2.metric("Target Weight", f"{u_weight - 2 if 'Marathon' in u_goal else u_weight}kg")
m3.metric("Training Load", "Optimal", delta="12%", delta_color="normal")

tabs = st.tabs(["🚀 Today's Session", "🥗 Smart Fueling", "📈 Performance Insights", "🤖 Coach AI"])

# --- TAB 1: SMART WORKOUT GENERATOR ---
with tabs[0]:
    st.subheader(f"Phase: {phase}")
    
    with st.container():
        if "Hyrox" in u_goal:
            is_pro = "Pro" in u_goal
            sled_weight = 175 if is_pro else 125 # Standard Hyrox weights
            
            st.markdown(f"### ⚡ Hybrid Session: Interfacing")
            st.info(f"**Coach Note:** Focus on the transition from the Sled to the run. Don't let your legs 'heavy up'.")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Functional Power**")
                st.checkbox(f"Sled Push: 4 x 20m ({sled_weight}kg)")
                st.checkbox("Burpee Broad Jumps: 80m")
                st.checkbox("Sandbag Lunges: 100m (20/30kg)")
            with col2:
                st.write("**Aerobic Capacity**")
                st.checkbox("1km Run @ Target Race Pace")
                st.checkbox("1km Row @ 2:00/500m")
                st.checkbox("1km Run (Repeat)")
                
        elif "Marathon" in u_goal:
            st.markdown("### 🏃‍♂️ Endurance Session: Zone 2")
            st.info("**Coach Note:** Keep heart rate below 145bpm. Build the aerobic engine.")
            st.checkbox("12km Steady State Run")
            st.checkbox("Post-Run: 3x15 Single Leg Calf Raises")
            st.checkbox("Post-Run: 5 min Hip Mobility")

    st.divider()
    if st.button("LOG WORKOUT AS COMPLETE"):
        st.balloons()
        st.toast("Data synced with Gym Owner Dashboard!")

# --- TAB 2: PRECISION NUTRITION ---
with tabs[1]:
    st.subheader("Dynamic Macro Breakdown")
    # Mifflin-St Jeor simplified for UI
    base_calories = (10 * u_weight) + 900 
    activity_mult = {"Base Building": 1.4, "Peak Intensity": 1.7, "Tapering / Recovery": 1.2}[phase]
    daily_target = int(base_calories * activity_mult)

    c1, c2, c3 = st.columns(3)
    c1.metric("Daily Calories", f"{daily_target} kcal")
    c2.metric("Protein (g)", f"{int(u_weight * 2.2)}")
    c3.metric("Carbs (g)", f"{int((daily_target * 0.55)/4)}")
    
    st.write("#### Nutrition Strategy")
    if "Hyrox" in u_goal:
        st.warning("High intensity detected. Increase electrolyte intake by 500mg today.")
    else:
        st.success("Endurance focus. Aim for 60g of carbs per hour during your long run.")

# --- TAB 3: ANALYTICS ---
with tabs[2]:
    st.subheader("Long-term Athlete Progress")
    # Generate realistic fake data
    dates = pd.date_range(start="2024-01-01", periods=10)
    data = pd.DataFrame({
        'Fitness Score': np.linspace(60, 95, 10) + np.random.randn(10) * 2,
        'Fatigue': np.linspace(20, 45, 10) + np.random.randn(10) * 5
    }, index=dates)
    
    st.line_chart(data)
    st.caption("Tracking Fitness (Blue) vs Fatigue (Yellow).")

# --- TAB 4: COACH AI ---
with tabs[3]:
    st.subheader("24/7 Virtual Strength Coach")
    msg = st.chat_message("assistant")
    msg.write(f"Hello {u_name}! I see you are in the **{phase}** phase of your **{u_goal}** journey. How is your recovery feeling today?")
    
    chat_input = st.text_input("Ask a question (e.g., 'My knees hurt' or 'I missed my run')")
    if chat_input:
        st.chat_message("user").write(chat_input)
        if "hurt" in chat_input.lower() or "pain" in chat_input.lower():
            st.chat_message("assistant").write("Stop immediately. I recommend swapping today's session for low-impact swimming and 15 mins of foam rolling. I will notify your gym coach.")
        else:
            st.chat_message("assistant").write("Keep pushing! Your data shows you are recovering well. Stick to the plan.")

