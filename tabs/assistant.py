import streamlit as st
from tabs.nutrition import generate_weekly_plan

def render_assistant_tab(u_goal, u_weight):
    st.title("🧠 Nexus AI Assistant")
    st.write("Ask to change your diet, or for training advice.")

    user_query = st.chat_input("Tell me to change your plan (e.g. 'I am vegan now')")

    if user_query:
        st.chat_message("user").write(user_query)
        
        # LOGIC: Check if they want to change the plan
        if any(x in user_query.lower() for x in ["vegan", "meal", "diet", "plan", "food", "eat"]):
            with st.spinner("Rewriting your entire 7-day plan..."):
                # Global update
                new_plan = generate_weekly_plan(u_goal, u_weight, user_query)
                if new_plan:
                    st.session_state.weekly_meals = new_plan
                    st.success("✅ Nutrition Plan Updated! Check the Nutrition Tab.")
                else:
                    st.error("AI was unable to format the plan. Try again.")
        else:
            st.chat_message("assistant").write("I'm here to help with training or nutrition. For meal changes, just ask!")
