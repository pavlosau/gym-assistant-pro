import streamlit as st
from tabs.nutrition import generate_weekly_plan
from tabs.workout import generate_workout_plan

def render_assistant_tab(context):
    st.title("🧠 Nexus AI Assistant")
    st.info("I use your age, weight, and injury profile to customize responses.")

    user_query = st.chat_input("Ask for a change (e.g., 'Make my workout 30 mins' or 'I'm vegan')")

    if user_query:
        st.chat_message("user").write(user_query)
        q = user_query.lower()
        
        # Check for Workout keywords
        if any(x in q for x in ["workout", "exercise", "training", "hurt", "equipment", "pain"]):
            with st.spinner("AI Coach is re-calculating for your profile..."):
                # We pass the whole context dictionary here
                st.session_state.current_workout = generate_workout_plan(context, user_query)
                st.success("✅ Workout Updated! Check the Workout tab.")
        
        # Check for Nutrition keywords
        elif any(x in q for x in ["vegan", "meal", "diet", "plan", "food", "calories"]):
            with st.spinner("AI Nutritionist is adjusting your macros..."):
                # We pass the whole context dictionary here
                st.session_state.weekly_meals = generate_weekly_plan(context, user_query)
                st.success("✅ Nutrition Plan Updated! Check the Nutrition tab.")
        else:
            st.chat_message("assistant").write("I can help adjust your plan. Try asking for a specific diet change or exercise swap.")
