import streamlit as st
import datetime
import random
from tabs.workout import render_workout_tab
from tabs.nutrition import render_nutrition_tab, generate_weekly_plan # You can move generate_weekly_plan to nutrition.py too
from tabs.analytics import render_analytics_tab

# --- AUTH LOGIC ---
st.set_page_config(page_title="Nexus Hybrid OS", layout="wide", page_icon="⚡")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # (Insert your Login Screen Code Here)
    st.title("⚡ Nexus Hybrid OS")
    if st.button("Log In (Demo)"):
        st.session_state.logged_in = True
        st.rerun()
else:
    # --- APP START ---
    st.sidebar.title("👤 Athlete Profile")
    u_name = st.sidebar.text_input("Name", "Alex")
    u_goal = st.sidebar.selectbox("Goal", ["Hyrox Pro", "Marathon Prep"])
    u_weight = st.sidebar.number_input("Weight (kg)", 40, 150, 85)
    u_level = st.sidebar.select_slider("Level", ["Foundation", "Performance", "Elite"])
    days_to_race = st.sidebar.number_input("Days to Race", 1, 100, 30)
    
    intensity_mod = {"Foundation": 0.9, "Performance": 1.1, "Elite": 1.3}[u_level]

    # Initialize Meal State
    if 'weekly_meals' not in st.session_state:
        # Note: You'll need to move your generate_weekly_plan function to nutrition.py
        from tabs.nutrition import generate_weekly_plan
        st.session_state.weekly_meals = generate_weekly_plan(u_goal)

    tabs = st.tabs(["🚀 WORKOUT", "🥗 NUTRITION", "📊 ANALYTICS"])

    with tabs[0]:
        render_workout_tab(u_goal, u_level, intensity_mod, days_to_race)

    with tabs[1]:
        render_nutrition_tab(u_name, u_goal, u_weight, intensity_mod)

    with tabs[2]:
        render_analytics_tab(u_name, u_goal, days_to_race)
