import streamlit as st
import google.generativeai as genai
import json
import random

# Initialize Gemini (Make sure your API Key is in Streamlit Secrets)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Gemini API Key missing in Secrets!")

def generate_weekly_plan(goal, weight=85, requirements="None"):
    """This is the function app.py is looking for."""
    prompt = f"""
    Generate a 7-day meal plan for a {weight}kg athlete training for {goal}.
    Requirements: {requirements}
    Return ONLY a JSON object:
    {{
      "Mon": {{"Breakfast": "...", "Lunch": "...", "Dinner": "..."}},
      "Tue": {{...}}, "Wed": {{...}}, "Thu": {{...}}, "Fri": {{...}}, "Sat": {{...}}, "Sun": {{...}}
    }}
    """
    try:
        response = model.generate_content(prompt)
        # Strip potential markdown backticks from AI response
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except:
        # Fallback if AI fails or API key is wrong
        return {day: {"Breakfast": "Oats", "Lunch": "Chicken", "Dinner": "Steak"} for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}

def render_nutrition_tab(u_name, u_goal, u_weight, intensity_mod):
    st.title("🥗 Gemini AI Nutritionist")
    
    # AI Update Interface
    with st.expander("🪄 Ask AI to modify your meals"):
        change_req = st.text_input("e.g., 'I am vegan this week' or 'Increase calories'")
        if st.button("Update Plan with Gemini"):
            st.session_state.weekly_meals = generate_weekly_plan(u_goal, u_weight, change_req)
            st.rerun()

    # Display the Plan
    if st.session_state.weekly_meals:
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        cols = st.columns(7)
        for i, day in enumerate(days):
            with cols[i]:
                st.markdown(f"### {day}")
                day_data = st.session_state.weekly_meals.get(day, {})
                for meal in ["Breakfast", "Lunch", "Dinner"]:
                    st.caption(meal)
                    st.write(day_data.get(meal, "Pending..."))
                st.write("---")
