import streamlit as st
import google.generativeai as genai
import json
import re

# Gemini Config
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Gemini API Key missing in Settings > Secrets!")

def generate_weekly_plan(goal, weight, requirements="None"):
    prompt = f"""
    Create a 7-day high-performance meal plan for a {weight}kg athlete training for {goal}.
    Specific Requests: {requirements}
    
    Return ONLY a raw JSON object. No conversational text.
    Format:
    {{
      "Mon": {{"Breakfast": "...", "Lunch": "...", "Dinner": "..."}},
      "Tue": {{...}}, "Wed": {{...}}, "Thu": {{...}}, "Fri": {{...}}, "Sat": {{...}}, "Sun": {{...}}
    }}
    """
    try:
        response = model.generate_content(prompt)
        # Find JSON block
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {day: {"Breakfast": "Oats", "Lunch": "Chicken", "Dinner": "Steak"} for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}
    except:
        return {day: {"Breakfast": "Oats", "Lunch": "Chicken", "Dinner": "Steak"} for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}

def render_nutrition_tab(u_name, u_goal, u_weight, intensity_mod):
    st.title("🥗 Gemini AI Nutritionist")
    
    # Update Plan via Chat
    with st.expander("🪄 Ask AI to Change the Plan"):
        user_req = st.text_input("e.g., 'Make it vegan', 'I don't like fish', 'Add more carbs'")
        if st.button("Update My Plan"):
            with st.spinner("Gemini is adjusting your requirements..."):
                st.session_state.weekly_meals = generate_weekly_plan(u_goal, u_weight, user_req)
                st.rerun()

    # Display Grid
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
