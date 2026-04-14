import streamlit as st
import pandas as pd
import numpy as np

def render_analytics_tab(u_name, u_goal, u_weight):
    st.subheader("📊 Performance Lab")
    st.line_chart(np.random.randn(15, 2))
    
    st.divider()
    st.subheader("🧠 Nexus AI Assistant")
    
    # Cross-tab communication
    user_query = st.chat_input("Ask me anything...")
    if user_query:
        if any(word in user_query.lower() for word in ["meal", "food", "plan", "diet"]):
            from tabs.nutrition import generate_weekly_plan
            with st.spinner("Updating your nutrition plan..."):
                st.session_state.weekly_meals = generate_weekly_plan(u_goal, u_weight, user_query)
                st.success("Plan updated! Head to the Nutrition tab to see your new meals.")
        else:
            st.write(f"🤖 **Coach:** Focusing on your {u_goal} progress, {u_name}. Make sure you're sleeping 8 hours tonight.")
