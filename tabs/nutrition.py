import streamlit as st
import google.generativeai as genai
import json
import re

def generate_weekly_plan(context, requirements="None"):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Create a 7-day meal plan. 
    Profile: {context['age']}yo, {context['height']}cm, {context['weight']}kg. 
    Goal: {context['goal']}. Activity: {context['activity']}.
    User Requests: {requirements}

    Return ONLY JSON: {{"Mon": {{"Breakfast": "...", "Lunch": "...", "Dinner": "..."}}, ...}}
    """
    try:
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group())
    except:
        return None

def render_nutrition_tab(name, context):
    st.header(f"🥗 {name}'s Bio-Individual Plan")
    st.caption(f"Targeting {context['goal']} at {context['weight']}kg")
    # ... display logic same as before ...
