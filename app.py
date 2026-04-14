import streamlit as st
import datetime
import pandas as pd
import numpy as np

# --- 1. INITIALIZATION & SESSION STATE ---
# This prevents the app from "forgetting" your progress when you toggle settings
if 'workouts_completed' not in st.session_state:
    st.session_state.workouts_completed = 0
if 'calories_consumed' not in st.session_state:
    st.session_state.calories_consumed = 0

st.set_page_config(page_title="Nexus Hybrid OS", layout="centered", page_icon="⚡")

# --- 2. MULTI-TENANT BRANDING ENGINE ---
PARTNERS = {
    "Nexus Individual": {"color": "#00E5FF", "bg": "#001214", "logo": "💠"},
    "Iron Forge Gym": {"color": "#FF3D00", "bg": "#120500", "logo": "⚒️"},
    "Zenith Athletics": {"color": "#7C4DFF", "bg": "#090014", "logo": "🏔️"},
    "Carbon Performance": {"color": "#00E676", "bg": "#000D05", "logo": "🔌"}
}

st.sidebar.header("🛡️ Secure Access")
gym_choice = st.sidebar.selectbox("Partner Portal", list(PARTNERS.keys()))
brand = PARTNERS[gym_choice]

# --- 3. PREMIUM UI STYLING ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #050505; color: #E0E0E0; }}
    [data-testid="stMetricValue"] {{ color: {brand['color']}; font-family: 'Inter', sans-serif; font-weight: 800; }}
    .stButton>button {{ 
        background: linear-gradient(90deg, {brand['color']} 0%, {brand['bg']} 100%); 
        color: white; border: 1px solid {brand['color']}; border-radius: 12px; height: 3.8rem;
        font-size: 1.1rem; letter-spacing: 1px; transition: 0.5s;
    }}
    .stButton>button:hover {{ box-shadow: 0px 0px 15px {brand['color']}; transform: scale(1.02); }}
    div[data-testid="stExpander"] {{ border: 1px solid #222; border-radius: 12px; background: #0F0F0F; padding: 10px; }}
    .stProgress > div > div > div > div {{ background-color: {brand['color']}; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. ATHLETE INTELLIGENCE SIDEBAR ---
st.sidebar.divider()
st.sidebar.subheader("Athlete Intelligence")
u_name = st.sidebar.text_input("Athlete Name", "Alex")
u_weight = st.sidebar.number_input("Mass (kg)", 40, 160, 85)
u_goal = st.sidebar.selectbox("Event", ["Hyrox Pro", "Hyrox Open", "Marathon", "Half-Marathon"])
u_level = st.sidebar.select_slider("Intensity Level", ["Active Recovery", "Foundation", "Performance", "Elite"])

days_to_race = st.sidebar.number_input("Days to Event", 1, 365, 60)
intensity_mod = {"Active Recovery": 0.7, "Foundation": 0.9, "Performance": 1.1, "Elite": 1.3}[u_level]

# --- 5. MAIN DASHBOARD ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title(f"{brand['logo']} {gym_choice}")
    st.write(f"**Current Athlete:** {u_name}")
with col_h2:
    st.metric("Race Countdown", f"{days_to_race}d")

tabs = st.tabs(["🚀 DAILY WORKOUT", "🥗 PRECISION FUEL", "📊 ANALYTICS", "🧠 AI COACH"])

# --- TAB 1: DYNAMIC WORKOUTS ---
with tabs[0]:
    st.subheader("Targeted Session")
    
    # Injury Screening Feature (High-end addition)
    with st.expander("⚠️ Pre-Workout Health Check"):
        soreness = st.slider("Muscle Soreness (1-10)", 1, 10, 3)
        if soreness > 7:
            st.error("High fatigue detected. Today's weights reduced by 20% for safety.")
            intensity_mod *= 0.8

    if "Hyrox" in u_goal:
        base_sled = 175 if "Pro" in u_goal else 125
        st.markdown(f"#### **Hybrid Engine: The {u_level} Protocol**")
        
        c1, c2 = st.columns(2)
        with c1:
            st.info("Power / Strength")
            st.checkbox(f"Sled Push: 4x20m @ {int(base_sled * intensity_mod)}kg")
            st.checkbox(f"Kettlebell Lunges: 100m @ {int(24 * intensity_mod)}kg")
        with c2:
            st.info("Aerobic Interfacing")
            st.checkbox(f"Interval Run: 4 x 1km @ {(5.0 - (intensity_mod * 0.5)):.2f} min/km")
            st.checkbox("Ski-Erg: 1000m (Target Pace)")

    elif "Marathon" in u_goal:
        dist = (12 if days_to_race > 14 else 5) * intensity_mod
        st.markdown(f"#### **Endurance Base: Zone 2 Focus**")
        st.checkbox(f"Long Run: {dist:.1f} km")
        st.checkbox("Drills: 3x50m A-Skips & B-Skips")
    
    if st.button("LOG SESSION AS COMPLETE"):
        st.session_state.workouts_completed += 1
        st.balloons()
        st.success(f"Success! You have completed {st.session_state.workouts_completed} sessions this month.")

# --- TAB 2: NUTRITION & RECOVERY ---
with tabs[1]:
    st.subheader("Metabolic Tracking")
    # Mifflin-St Jeor + dynamic load
    bmr = (10 * u_weight) + 900
    daily_cal = int(bmr * (1.3 if soreness < 5 else 1.1) * intensity_mod)
    
    nc1, nc2, nc3 = st.columns(3)
    nc1.metric("Calories", f"{daily_cal}")
    nc2.metric("Protein", f"{int(u_weight * 2.2)}g")
    nc3.metric("Carbs", f"{int((daily_cal * 0.55)/4)}g")
    
    st.divider()
    if st.button("Add 500kcal Meal"):
        st.session_state.calories_consumed += 500
    
    st.progress(min(st.session_state.calories_consumed / daily_cal, 1.0), 
                text=f"Fueling Progress: {st.session_state.calories_consumed} / {daily_cal} kcal")

# --- TAB 3: PERFORMANCE DATA ---
with tabs[2]:
    st.subheader("The Lab: Data Trends")
    
    # Realistic Synthetic Growth Data
    chart_days = pd.date_range(end=datetime.date.today(), periods=20)
    perf_data = pd.DataFrame({
        "VO2 Max Estimate": np.linspace(45, 52, 20) + np.random.randn(20) * 0.5,
        "Strength Index": np.linspace(100, 140, 20) + np.random.randn(20) * 2
    }, index=chart_days)
    
    st.line_chart(perf_data)
    
    col_a, col_b = st.columns(2)
    col_a.metric("Workout Consistency", "94%", "+2%")
    col_b.metric("Avg. Sleep Quality", "82/100", "-5%")

# --- TAB 4: THE AI ASSISTANT ---
with tabs[3]:
    st.subheader("Nexus AI Assistant")
    st.chat_message("assistant").write(f"Hello {u_name}. I am monitoring your {u_goal} progress. You are {days_to_race} days from the start line. How are your energy levels today?")
    
    query = st.text_input("Describe how you feel (e.g. 'My calves are tight' or 'I want more power')")
    if query:
        with st.spinner("Processing Bio-metrics..."):
            if "tight" in query or "sore" in query:
                st.warning("⚠️ Recommendation: Swap tomorrow's run for 20 mins of eccentric heel drops and 15 mins of infra-red sauna/heat therapy.")
            else:
                st.success(f"Logic confirmed. Based on your {u_level} status, we will increase sled volume by 5% next week.")

# --- FOOTER ---
st.markdown("---")
st.caption(f"© 2026 Nexus Hybrid OS | Licensed to {gym_choice} | v2.0.4 Premium")
