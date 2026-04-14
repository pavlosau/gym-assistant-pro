import streamlit as st
import google.generativeai as genai
from tabs.workout import render_workout_tab, generate_workout_plan
from tabs.nutrition import render_nutrition_tab, generate_weekly_plan
from tabs.assistant import render_assistant_tab
from tabs.analytics import render_analytics_tab

# --- PERSISTENT LOGIN CHECK ---
if "logged_in" not in st.session_state:
    # Check if the URL has a 'login' parameter
    if st.query_params.get("auth") == "success":
        st.session_state.logged_in = True
    else:
        st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("⚡ Nexus Hybrid OS")
    email = st.text_input("Email")
    pw = st.text_input("Password", type="password")
    if st.button("Log In"):
        if email == "user@test.com" and pw == "1234":
            st.session_state.logged_in = True
            st.query_params["auth"] = "success" # Saves to URL
            st.rerun()
else:
    # --- DETAILED ATHLETE PROFILE ---
    st.sidebar.title("👤 Athlete Intelligence")
    u_name = st.sidebar.text_input("Full Name", "Alex")
    
    col1, col2 = st.sidebar.columns(2)
    u_age = col1.number_input("Age", 14, 90, 28)
    u_height = col2.number_input("Height (cm)", 120, 230, 175)
    
    u_weight = st.sidebar.number_input("Current Weight (kg)", 40.0, 200.0, 82.5)
    u_goal = st.sidebar.selectbox("Primary Goal", ["Fat Loss", "Muscle Gain", "Hyrox Performance", "Endurance"])
    u_activity = st.sidebar.select_slider("Activity Level", ["Sedentary", "Moderate", "Active", "Pro"])
    u_injuries = st.sidebar.text_area("Injuries / Limitations", "None")

    # Combine data into a single context string for the AI
    athlete_context = {
        "age": u_age, "height": u_height, "weight": u_weight,
        "goal": u_goal, "activity": u_activity, "injuries": u_injuries
    }

    # --- AI INITIALIZATION (Pass the detailed context) ---
    if st.session_state.get('weekly_meals') is None:
        with st.spinner("Calculating Macros..."):
            st.session_state.weekly_meals = generate_weekly_plan(athlete_context)
            
    if st.session_state.get('current_workout') is None:
        with st.spinner("Building Periodized Plan..."):
            st.session_state.current_workout = generate_workout_plan(athlete_context)

    # --- UI TABS ---
    tabs = st.tabs(["🚀 WORKOUT", "🥗 NUTRITION", "📊 ANALYTICS", "🧠 ASSISTANT"])
    with tabs[0]: render_workout_tab(athlete_context)
    with tabs[1]: render_nutrition_tab(u_name, athlete_context)
    with tabs[2]: render_analytics_tab()
    with tabs[3]: render_assistant_tab(athlete_context)

    if st.sidebar.button("Logout & Clear Session"):
        st.query_params.clear()
        st.session_state.clear()
        st.rerun()
