import streamlit as st
import google.generativeai as genai
import json
import re

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key missing.")

def generate_weekly_plan(goal, weight, requirements="None"):
    # STRICT PROMPT: Forces the AI to prioritize requirements
    prompt = f"""
    ROLE: Expert Performance Nutritionist.
    USER GOAL: {goal} ({weight}kg)
    STRICT DIETARY RESTRICTION: {requirements}

    TASK: Generate a 7-day meal plan. 
    IF THE USER REQUESTS VEGAN, YOU MUST NOT INCLUDE MEAT, DAIRY, OR EGGS.
    
    RETURN ONLY RAW JSON:
    {{
      "Mon": {{"Breakfast": "...", "Lunch": "...", "Dinner": "..."}},
      "Tue": {{...}}, "Wed": {{...}}, "Thu": {{...}}, "Fri": {{...}}, "Sat": {{...}}, "Sun": {{...}}
    }}
    """
    try:
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except:
        return None

def render_nutrition_tab(u_name, u_goal, u_weight, intensity_mod):
    st.title("🥗 Precision Nutrition")
    
    # Grid Display
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
