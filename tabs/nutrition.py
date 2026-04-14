import streamlit as st
import google.generativeai as genai
import json
import re

# Initialize Gemini
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key Error. Check your Streamlit Secrets.")

def generate_weekly_plan(goal, weight=85, requirements="None"):
    prompt = f"""
    Create a 7-day meal plan for a {weight}kg athlete training for {goal}.
    Requirements: {requirements}
    
    IMPORTANT: Return ONLY raw JSON. No conversational text.
    Structure:
    {{
      "Mon": {{"Breakfast": "text", "Lunch": "text", "Dinner": "text"}},
      "Tue": {{...}}, "Wed": {{...}}, "Thu": {{...}}, "Fri": {{...}}, "Sat": {{...}}, "Sun": {{...}}
    }}
    """
    try:
        response = model.generate_content(prompt)
        # Use Regex to find the JSON block in case AI adds chatter
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            raise ValueError("No JSON found")
    except Exception as e:
        # Emergency Fallback so the app doesn't show a Red Error
        return {day: {"Breakfast": "Protein Oats", "Lunch": "Chicken & Rice", "Dinner": "Salmon & Greens"} 
                for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}

def render_nutrition_tab(u_name, u_goal, u_weight, intensity_mod):
    st.title("🥗 AI Nutritionist (Gemini)")
    
    # 1. Update Section
    with st.expander("💬 Request Meal Changes"):
        user_req = st.text_input("e.g. 'I want more Mediterranean meals' or 'I am vegetarian'")
        if st.button("Update Plan"):
            with st.spinner("Gemini is rewriting your plan..."):
                st.session_state.weekly_meals = generate_weekly_plan(u_goal, u_weight, user_req)
                st.rerun()

    # 2. Display Section
    if st.session_state.weekly_meals:
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        cols = st.columns(7)
        for i, day in enumerate(days):
            with cols[i]:
                st.markdown(f"### {day}")
                day_meals = st.session_state.weekly_meals.get(day, {})
                for m_type in ["Breakfast", "Lunch", "Dinner"]:
                    st.caption(m_type)
                    st.write(day_meals.get(m_type, "N/A"))
                st.write("---")
