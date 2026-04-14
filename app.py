import streamlit as st
import datetime

# Attempt to import modular files
try:
    from tabs.workout import render_workout_tab
    from tabs.nutrition import render_nutrition_tab, generate_weekly_plan
    from tabs.analytics import render_analytics_tab
except Exception as e:
    st.error(f"Import Error: {e}")
    st.info("Check if 'tabs' folder has __init__.py and all .py files are present.")
    st.stop()

st.set_page_config(page_title="Nexus Hybrid OS", layout="wide", page_icon="⚡")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'weekly_meals' not in st.session_state:
    st.session_state.weekly_meals = None

if not st.session_state.logged_in:
    st.title("⚡ Nexus Hybrid OS")
    email = st.text_input("Email")
    pw = st.text_input("Password", type="password")
    if st.button("Log In"):
        if email == "user@test.com" and pw == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Use user@test.com / 1234")
else:
    st.sidebar.title("👤 Profile")
    u_name = st.sidebar.text_input("Name", "Alex")
    u_goal = st.sidebar.selectbox("Goal", ["Hyrox Pro", "Marathon Prep"])
    u_weight = st.sidebar.number_input("Weight (kg)", 40, 150, 85)
    u_level = st.sidebar.select_slider("Level", ["Foundation", "Performance", "Elite"])
    
    intensity_mod = {"Foundation": 0.9, "Performance": 1.1, "Elite": 1.3}[u_level]

    if st.session_state.weekly_meals is None:
        st.session_state.weekly_meals = generate_weekly_plan(u_goal)

    tabs = st.tabs(["🚀 WORKOUT", "🥗 NUTRITION", "📊 ANALYTICS"])

    with tabs[0]:
        render_workout_tab(u_goal, u_level, intensity_mod, 30)
    with tabs[1]:
        render_nutrition_tab(u_name, u_goal, u_weight, intensity_mod)
    with tabs[2]:
        render_analytics_tab(u_name, u_goal, 30)

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
