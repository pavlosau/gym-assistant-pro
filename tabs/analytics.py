def render_analytics_tab(u_name, u_goal, u_weight):
    st.subheader("🧠 Assistant Intelligence")
    
    query = st.chat_input("Ask me anything or request plan changes...")
    if query:
        # Check if they are asking for a meal change
        if "meal" in query.lower() or "plan" in query.lower() or "food" in query.lower():
             from tabs.nutrition import get_ai_meal_plan
             st.session_state.weekly_meals = get_ai_meal_plan(u_goal, u_weight, query)
             st.success("Nutrition Plan updated! Go to the Nutrition tab to see changes.")
        else:
             # Regular AI chat
             st.write("🤖 Assistant: I've processed your request.")
