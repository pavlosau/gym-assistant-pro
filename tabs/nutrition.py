import streamlit as st
import google.generativeai as genai
import json
import re

# Gemini Config
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Missing Gemini API Key in Secrets!")

def generate_weekly_plan(goal, weight, requirements="None"):
    prompt = f"""
    Create a 7-day meal plan for a {weight}kg athlete training for {goal}.
    DIETARY RESTRICTON: {requirements}
    
    IF THE REQUIREMENT IS VEGAN, YOU MUST NOT INCLUDE MEAT, DAIRY, OR EGGS.
    Return ONLY a raw JSON object. No conversational text.
    {{
      "Mon": {{"Breakfast": "...", "Lunch": "...", "Dinner": "..."}},
      "Tue": {{...}}, "Wed": {{...}}, "Thu": {{...}}, "Fri": {{...}}, "Sat": {{...}}, "Sun": {{...}}
    }}
    """
    try:
        response = model.generate_content(prompt)
        text = response.text
        # Clean JSON from AI chatter
        text = text.replace("```json", "").replace("```", "").strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except Exception as e:
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
                st.write("---")
