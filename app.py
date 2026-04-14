import streamlit as st
import datetime

# --- 1. SECURE IMPORTS ---
try:
    from tabs.workout import render_workout_tab
    from tabs.nutrition import render_nutrition_tab, generate_weekly_plan # <--- MUST MATCH
    from tabs.analytics import render_analytics_tab
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.stop()

st.set_page_config(page_title="Nexus Hybrid OS", layout="wide")

# --- 2. AUTH & SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'weekly_meals' not in st.session_state:
    st.session_state.weekly_meals = None

if not st.session_state.logged_in:
    # --- LOGIN SCREEN ---
    st.title("⚡ Nexus Login")
    user_mail = st.text_input("Email")
    user_pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user_mail == "user@test.com" and user_pw == "1234":
            st.session_state.logged_in = True
            st.rerun()
else:
    # --- MAIN APP ---
    st.sidebar.title("Athlete Profile")
    u_name = st.sidebar.text_input("Name", "Alex")
    u_goal = st.sidebar.selectbox("Goal", ["Hyrox Pro", "Marathon"])
    u_weight = st.sidebar.number_input("Weight (kg)", 40, 150, 85)
    
    # Initialize plan using Gemini if it's the first time
    if st.session_state.weekly_meals is None:
        with st.spinner("Gemini is creating your plan..."):
            st.session_state.weekly_meals = generate_weekly_plan(u_goal, u_weight)

    tabs = st.tabs(["🚀 WORKOUT", "🥗 NUTRITION", "📊 ANALYTICS"])

    with tabs[0]:
        render_workout_tab(u_goal, "Performance", 1.1, 30)
    with tabs[1]:
        render_nutrition_tab(u_name, u_goal, u_weight, 1.1)
    with tabs[2]:
        render_analytics_tab(u_name, u_goal, 30)
