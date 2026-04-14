import streamlit as st
import google.generativeai as genai
import json, re

def generate_weekly_plan(context, req="None"):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"7-day meal plan for {context}. JSON only: {{'Mon': {{'Breakfast': '...', 'Lunch': '...', 'Dinner': '...'}}}}"
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group())
    except:
        # FALLBACK PLAN - Appears if API Fails
        return {day: {"Breakfast": "Oats & Protein", "Lunch": "Chicken & Rice", "Dinner": "Salmon & Greens"} 
                for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}

def render_nutrition_tab(name, context):
    st.header(f"🥗 {name}'s Plan")
    if st.session_state.weekly_meals:
        cols = st.columns(7)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            with cols[i]:
                st.write(f"**{day}**")
                meals = st.session_state.weekly_meals.get(day, {})
                st.caption(f"B: {meals.get('Breakfast')}")
                st.caption(f"L: {meals.get('Lunch')}")
                st.caption(f"D: {meals.get('Dinner')}")
