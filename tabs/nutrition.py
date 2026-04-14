import streamlit as st
import google.generativeai as genai
import json
import re

def generate_weekly_plan(goal, weight, requirements="None"):
    if "GEMINI_API_KEY" not in st.secrets: return None
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Create a 7-day meal plan for a {weight}kg athlete training for {goal}.
    DIETARY RESTRICTION: {requirements}
    IF VEGAN, NO MEAT/DAIRY.
    Return ONLY raw JSON:
    {{ "Mon": {{"Breakfast": "...", "Lunch": "...", "Dinner": "..."}}, ... }}
    """
    try:
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except:
        return None

def render_nutrition_tab(u_name, u_goal, u_weight):
    st.title("🥗 Precision Nutrition")
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
