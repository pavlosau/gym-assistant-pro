import streamlit as st
import google.generativeai as genai
import json, re

def generate_workout_plan(context, req="None"):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Workout for {context}. JSON only: {{'name': 'Title', 'blocks': [{{'name': 'Warmup', 'exercises': []}}]}}"
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group())
    except:
        return {"name": "Basic Full Body", "blocks": [{"name": "Circuit", "exercises": ["Pushups", "Squats", "Plank"]}]}

def render_workout_tab(context):
    work = st.session_state.current_workout
    if work:
        st.header(f"🔥 {work.get('name')}")
        for block in work.get('blocks', []):
            st.subheader(block.get('name'))
            for ex in block.get('exercises', []):
                st.checkbox(ex)
