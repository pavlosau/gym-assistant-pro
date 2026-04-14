import streamlit as st
import google.generativeai as genai
import datetime

# --- SECURE IMPORTS ---
try:
    from tabs.workout import render_workout_tab, generate_workout_plan
    from tabs.nutrition import render_nutrition_tab, generate_weekly_plan
    from tabs.analytics import render_analytics_tab
    from tabs.assistant import render_assistant_tab
except ImportError as e:
    st.error(f"Module Import Error: {e}")
    st.stop()

# Configure AI globally for the main script
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets!")

st.set_page_config(page_title="Nexus Hybrid OS", layout="wide", page_icon="⚡")

# --- INITIALIZE STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'weekly_meals' not in st.session_state:
    st.session_state.weekly_meals = None
if 'current_workout' not in st.session_state:
    st.session_state.current_workout = None

if not st.session_state.logged_in:
    st.title("⚡ Nexus Hybrid OS")
    email = st.text_input("Email (user@test.com)")
    pw = st.text_input("Password (1234)", type="password")
    if st.button("Log In"):
        if email == "user@test.com" and pw == "1234":
            st.session_state.logged_in = True
            st.rerun()
else:
    # Sidebar
    st.sidebar.title("👤 Athlete Profile")
    u_name = st.sidebar.text_input("Name", "Alex")
    u_goal = st.sidebar.selectbox("Goal", ["Hyrox Pro", "Marathon Prep", "Elite Strength"])
    u_weight = st.sidebar.number_input("Weight (kg)", 40, 160, 85)
    u_level = st.sidebar.select_slider("Level", ["Foundation", "Performance", "Elite"])
    
    # Auto-generate plans if they don't exist
    if st.session_state.weekly_meals is None:
        with st.spinner("AI is crafting your nutrition..."):
            st.session_state.weekly_meals = generate_weekly_plan(u_goal, u_weight)
            
    if st.session_state.current_workout is None:
        with st.spinner("AI is drafting your workout..."):
            st.session_state.current_workout = generate_workout_plan(u_goal, u_level)

    # Tabs
    tabs = st.tabs(["🚀 WORKOUT", "🥗 NUTRITION", "📊 ANALYTICS", "🧠 AI ASSISTANT"])

    with tabs[0]:
        render_workout_tab(u_goal, u_level, u_weight)
    with tabs[1]:
        render_nutrition_tab(u_name, u_goal, u_weight)
    with tabs[2]:
        render_analytics_tab()
    with tabs[3]:
        render_assistant_tab(u_goal, u_weight, u_level)

    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
