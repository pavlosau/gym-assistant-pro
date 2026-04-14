import streamlit as st
import datetime

# --- IMPORTS ---
try:
    from tabs.workout import render_workout_tab
    from tabs.nutrition import render_nutrition_tab, generate_weekly_plan
    from tabs.analytics import render_analytics_tab
    from tabs.assistant import render_assistant_tab
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.stop()

st.set_page_config(page_title="Nexus Hybrid OS", layout="wide")

# --- STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'weekly_meals' not in st.session_state:
    st.session_state.weekly_meals = None

# --- AUTH ---
if not st.session_state.logged_in:
    st.title("⚡ Nexus Login")
    email = st.text_input("Email")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if email == "user@test.com" and pw == "1234":
            st.session_state.logged_in = True
            st.rerun()
else:
    # --- SIDEBAR ---
    st.sidebar.title("Athlete Profile")
    u_name = st.sidebar.text_input("Name", "Alex")
    u_goal = st.sidebar.selectbox("Goal", ["Hyrox Pro", "Marathon Prep"])
    u_weight = st.sidebar.number_input("Weight (kg)", 40, 160, 85)
    
    # Initialize plan
    if st.session_state.weekly_meals is None:
        st.session_state.weekly_meals = generate_weekly_plan(u_goal, u_weight)

    # --- THE 4 TABS ---
    tabs = st.tabs(["🚀 WORKOUT", "🥗 NUTRITION", "📊 ANALYTICS", "🧠 AI ASSISTANT"])

    with tabs[0]:
        render_workout_tab(u_goal, "Performance", 1.1)
    with tabs[1]:
        render_nutrition_tab(u_name, u_goal, u_weight, 1.1)
    with tabs[2]:
        render_analytics_tab()
    with tabs[3]:
        render_assistant_tab(u_goal, u_weight)
