import streamlit as st
from tabs.nutrition import generate_weekly_plan
from tabs.workout import generate_workout_plan

def render_assistant_tab(u_goal, u_weight, u_level):
    st.title("🧠 Nexus AI Assistant")
    query = st.chat_input("Ask for a new plan or specific change...")

    if query:
        st.chat_message("user").write(query)
        q = query.lower()
        
        if any(x in q for x in ["workout", "exercise", "hurt", "equipment"]):
            with st.spinner("Updating workout..."):
                st.session_state.current_workout = generate_workout_plan(u_goal, u_level, query)
                st.success("Workout Updated!")
        elif any(x in q for x in ["vegan", "meal", "diet", "food"]):
            with st.spinner("Updating nutrition..."):
                st.session_state.weekly_meals = generate_weekly_plan(u_goal, u_weight, query)
                st.success("Nutrition Plan Updated!")
        else:
            st.chat_message("assistant").write("Tell me more about the changes you need!")
