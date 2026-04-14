import streamlit as st
from tabs.nutrition import generate_weekly_plan
from tabs.workout import generate_workout_plan

def render_assistant_tab(u_goal, u_weight, u_level):
    st.title("🧠 Nexus AI Assistant")
    user_query = st.chat_input("How can I help with your training or diet?")

    if user_query:
        query = user_query.lower()
        st.chat_message("user").write(user_query)
        
        # LOGIC: Workout Swap
        if any(x in query for x in ["workout", "exercise", "training", "hurt", "equipment"]):
            with st.spinner("AI Coach is recalculating your training..."):
                st.session_state.current_workout = generate_workout_plan(u_goal, u_level, user_query)
                st.success("✅ Workout Updated! Check the Workout tab.")
        
        # LOGIC: Nutrition Swap
        elif any(x in query for x in ["vegan", "meal", "diet", "plan", "food"]):
            with st.spinner("AI Nutritionist is rewriting your plan..."):
                st.session_state.weekly_meals = generate_weekly_plan(u_goal, u_weight, user_query)
                st.success("✅ Nutrition Plan Updated! Check the Nutrition tab.")
