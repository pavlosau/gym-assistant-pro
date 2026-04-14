import streamlit as st
import datetime

# --- MODULAR IMPORTS ---
try:
    from tabs.workout import render_workout_tab
    from tabs.nutrition import render_nutrition_tab, generate_weekly_plan
    from tabs.analytics import render_analytics_tab
except ImportError as e:
    st.error(f"Module Import Error: {e}. Check your 'tabs' folder and __init__.py")
    st.stop()

st.set_page_config(page_title="Nexus Hybrid OS", layout="wide", page_icon="⚡")

# --- INITIALIZE SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'weekly_meals' not in st.session_state:
    st.session_state.weekly_meals = None

# --- LOGIN GATE ---
if not st.session_state.logged_in:
    st.title("⚡ Nexus Hybrid OS")
    email = st.text_input("Email (user@test.com)")
    pw = st.text_input("Password (1234)", type="password")
    if st.button("Log In"):
        if email == "user@test.com" and pw == "1234":
            st.session_state.logged_in = True
            st.rerun()
else:
    # --- ATHLETE SIDEBAR ---
    st.sidebar.title("👤 Athlete Profile")
    u_name = st.sidebar.text_input("Name", "Alex")
    u_goal = st.sidebar.selectbox("Goal", ["Hyrox Pro", "Marathon Prep", "Elite Strength"])
    u_weight = st.sidebar.number_input("Weight (kg)", 40, 160, 85)
    u_level = st.sidebar.select_slider("Level", ["Foundation", "Performance", "Elite"])
    
    intensity_mod = {"Foundation": 0.9, "Performance": 1.1, "Elite": 1.3}[u_level]

    # --- AI MEAL INITIALIZATION ---
    # Only runs once at startup
    if st.session_state.weekly_meals is None:
        with st.spinner("Gemini is crafting your initial plan..."):
            st.session_state.weekly_meals = generate_weekly_plan(u_goal, u_weight)

    # --- TABS INTERFACE ---
    tabs = st.tabs(["🚀 WORKOUT", "🥗 AI NUTRITION", "📊 ANALYTICS"])

    with tabs[0]:
        render_workout_tab(u_goal, u_level, intensity_mod)
    with tabs[1]:
        render_nutrition_tab(u_name, u_goal, u_weight, intensity_mod)
    with tabs[2]:
        render_analytics_tab(u_name, u_goal, u_weight)

    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
