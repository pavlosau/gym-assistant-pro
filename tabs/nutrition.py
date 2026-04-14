import streamlit as st
import google.generativeai as genai
import json
import re

# ... (API Config and generate_weekly_plan code here) ...

def render_nutrition_tab(u_name, u_goal, u_weight, intensity_mod):
    st.title("🥗 Precision Nutrition")
    
    # Grid Display logic
    if st.session_state.weekly_meals:
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        cols = st.columns(7)
        for i, day in enumerate(days):
            with cols[i]:
                st.markdown(f"### {day}")
                day_data = st.session_state.weekly_meals.get(day, {})
                for meal in ["Breakfast", "Lunch", "Dinner"]:
                    st.caption(meal)
                    st.write(day_data.get(meal, "N/A"))
