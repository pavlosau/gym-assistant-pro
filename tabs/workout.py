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

def generate_workout_plan(goal, level, requirements="None"):
    """Fetches a structured workout from Gemini."""
    prompt = f"""
    Create a professional workout session for an athlete.
    Goal: {goal}
    Current Level: {level}
    Specific Constraints/Equipment: {requirements}

    Return ONLY a raw JSON object. No conversational text.
    Format:
    {{
      "session_name": "Name of Workout",
      "blocks": [
        {{"block_name": "Warmup", "exercises": ["ex1", "ex2"]}},
        {{"block_name": "Main Set", "exercises": ["ex1", "ex2"]}},
        {{"block_name": "Cool Down", "exercises": ["ex1", "ex2"]}}
      ]
    }}
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except:
        return None

def render_workout_tab(u_goal, u_level, u_weight):
    st.title("🚀 AI Performance Coach")

    # 1. Initialize workout if empty
    if "current_workout" not in st.session_state or st.session_state.current_workout is None:
        with st.spinner("Coach is drafting today's session..."):
            st.session_state.current_workout = generate_workout_plan(u_goal, u_level)

    # 2. AI Modification Interface
    with st.expander("🛠️ Modify Session (AI Swap)"):
        swap_req = st.text_input("e.g., 'I don't have a pull-up bar', 'My lower back is sore', 'Make it shorter'")
        if st.button("Update Workout"):
            with st.spinner("Adjusting your session..."):
                new_workout = generate_workout_plan(u_goal, u_level, swap_req)
                if new_workout:
                    st.session_state.current_workout = new_workout
                    st.rerun()

    # 3. Display Workout
    if st.session_state.current_workout:
        work = st.session_state.current_workout
        st.subheader(f"🔥 {work.get('session_name', 'Daily Session')}")
        
        for block in work.get('blocks', []):
            with st.container():
                st.markdown(f"#### {block.get('block_name')}")
                for ex in block.get('exercises', []):
                    st.checkbox(ex, key=f"check_{ex}")
                st.write("")
