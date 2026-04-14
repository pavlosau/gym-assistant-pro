import streamlit as st
import google.generativeai as genai
import json
import re

def generate_workout_plan(context, requirements="None"):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Create a workout for an athlete:
    - Age: {context['age']}, Height: {context['height']}cm, Weight: {context['weight']}kg
    - Goal: {context['goal']}, Activity: {context['activity']}
    - Limitations: {context['injuries']}
    - User Request: {requirements}

    Rules: 
    1. If there are injuries, provide safer alternatives.
    2. Scale volume based on age and activity level.
    3. Return ONLY JSON structure: {{"session_name": "...", "blocks": [{{"block_name": "...", "exercises": []}}]}}
    """
    try:
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group())
    except:
        return None

def render_workout_tab(context):
    st.subheader(f"🔥 Daily Session for {context['goal']}")
    if st.session_state.current_workout:
        work = st.session_state.current_workout
        for block in work.get('blocks', []):
            st.write(f"**{block['block_name']}**")
            for ex in block['exercises']:
                st.checkbox(ex)
