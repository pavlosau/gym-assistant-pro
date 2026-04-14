import streamlit as st
import google.generativeai as genai
import json
import re

def generate_workout_plan(goal, level, requirements="None"):
    if "GEMINI_API_KEY" not in st.secrets: return None
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"Create a workout for {goal} at {level} level. Restrictions: {requirements}. Return ONLY JSON: {{'session_name': '...', 'blocks': [{{'block_name': '...', 'exercises': []}}]}}"
    try:
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except:
        return None

def render_workout_tab(u_goal, u_level, u_weight):
    st.title("🚀 AI Performance Coach")
    if st.session_state.current_workout:
        work = st.session_state.current_workout
        st.subheader(f"🔥 {work.get('session_name')}")
        for block in work.get('blocks', []):
            st.markdown(f"#### {block.get('block_name')}")
            for ex in block.get('exercises', []):
                st.checkbox(ex, key=f"ex_{ex}")
