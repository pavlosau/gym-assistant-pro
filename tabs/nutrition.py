import streamlit as st
import google.generativeai as genai
import json

# Setup Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def get_ai_meal_plan(goal, weight, requirements="None"):
    """Fetch a structured 7-day plan from Gemini."""
    prompt = f"""
    Generate a 7-day meal plan for an athlete.
    Athlete Goal: {goal}
    Weight: {weight}kg
    Additional Requirements: {requirements}
    
    Return ONLY a JSON object with this exact structure:
    {{
      "Mon": {{"Breakfast": "...", "Lunch": "...", "Dinner": "..."}},
      "Tue": {{...}},
      ...
    }}
    Include specific high-performance foods relevant to {goal}.
    """
    response = model.generate_content(prompt)
    # Clean up the response to ensure it's valid JSON
    json_str = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(json_str)

def render_nutrition_tab(u_name, u_goal, u_weight, intensity_mod):
    st.title("🥗 Gemini-Powered Nutrition")
    
    # Initialize plan if empty
    if "weekly_meals" not in st.session_state or st.session_state.weekly_meals is None:
        with st.spinner("Gemini is crafting your initial plan..."):
            st.session_state.weekly_meals = get_ai_meal_plan(u_goal, u_weight)

    # UI for updating via AI
    with st.expander("🧠 Chat with Nutritionist AI"):
        user_ask = st.text_input("Example: 'I'm traveling to Italy, make the plan Mediterranean style' or 'I'm allergic to nuts'")
        if st.button("Update My Plan"):
            with st.spinner("Gemini is adjusting your requirements..."):
                st.session_state.weekly_meals = get_ai_meal_plan(u_goal, u_weight, user_ask)
                st.success("Plan updated based on your request!")
                st.rerun()

    # Display the grid (Same as before but pulling from AI)
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
