import streamlit as st
from tabs.nutrition import generate_weekly_plan

def render_assistant_tab(u_goal, u_weight):
    st.title("🧠 Nexus AI Assistant")
    st.info("You can change your diet here. Try typing 'I am vegan now'.")

    user_query = st.chat_input("How can I help with your training or diet?")

    if user_query:
        st.chat_message("user").write(user_query)
        
        # Check if user wants a diet change
        keywords = ["vegan", "meal", "diet", "plan", "food", "meat", "allergic"]
        if any(x in user_query.lower() for x in keywords):
            with st.spinner("Gemini is rewriting your plan to match your request..."):
                new_plan = generate_weekly_plan(u_goal, u_weight, user_query)
                if new_plan:
                    st.session_state.weekly_meals = new_plan
                    st.success("✅ Nutrition Plan Updated! View it in the Nutrition tab.")
                else:
                    st.error("AI formatting error. Please try again.")
        else:
            st.chat_message("assistant").write("I've logged that. Let me know if you want to adjust your meal plan!")
