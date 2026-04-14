import streamlit as st
import google.generativeai as genai

# --- 1. SETTINGS & AUTH ---
st.set_page_config(page_title="Nexus Hybrid OS", layout="wide")

if "logged_in" not in st.session_state:
    if st.query_params.get("auth") == "success":
        st.session_state.logged_in = True
    else:
        st.session_state.logged_in = False

# Import tabs AFTER page config
from tabs.workout import render_workout_tab, generate_workout_plan
from tabs.nutrition import render_nutrition_tab, generate_weekly_plan
from tabs.assistant import render_assistant_tab
from tabs.analytics import render_analytics_tab

if not st.session_state.logged_in:
    st.title("⚡ Nexus Hybrid OS")
    email = st.text_input("Email")
    pw = st.text_input("Password", type="password")
    if st.button("Log In"):
        if email == "user@test.com" and pw == "1234":
            st.session_state.logged_in = True
            st.query_params["auth"] = "success"
            st.rerun()
else:
    # --- 2. ATHLETE PROFILE ---
    st.sidebar.title("👤 Profile")
    u_name = st.sidebar.text_input("Name", "Athlete")
    u_age = st.sidebar.number_input("Age", 18, 100, 30)
    u_weight = st.sidebar.number_input("Weight (kg)", 40, 200, 80)
    u_height = st.sidebar.number_input("Height (cm)", 100, 250, 180)
    u_goal = st.sidebar.selectbox("Goal", ["Muscle Gain", "Fat Loss", "Hyrox"])
    u_injuries = st.sidebar.text_input("Injuries", "None")

    athlete_context = {
        "age": u_age, "weight": u_weight, "height": u_height, 
        "goal": u_goal, "injuries": u_injuries
    }

    # --- 3. DATA INITIALIZATION ---
    if "weekly_meals" not in st.session_state or st.session_state.weekly_meals is None:
        st.session_state.weekly_meals = generate_weekly_plan(athlete_context)
    
    if "current_workout" not in st.session_state or st.session_state.current_workout is None:
        st.session_state.current_workout = generate_workout_plan(athlete_context)

    # --- 4. TABS ---
    t1, t2, t3, t4 = st.tabs(["🚀 WORKOUT", "🥗 NUTRITION", "📊 ANALYTICS", "🧠 AI"])
    with t1: render_workout_tab(athlete_context)
    with t2: render_nutrition_tab(u_name, athlete_context)
    with t3: render_analytics_tab()
    with t4: render_assistant_tab(athlete_context)
