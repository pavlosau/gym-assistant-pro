import streamlit as st
import pandas as pd
import numpy as np
import datetime

def render_analytics_tab(u_name, u_goal, days_to_race):
    st.subheader("Data Trend Analysis")
    chart_days = pd.date_range(end=datetime.date.today(), periods=15)
    data = pd.DataFrame({
        "Performance Index": np.linspace(60, 92, 15) + np.random.randn(15) * 3,
        "Recovery Score": np.random.randint(40, 95, 15)
    }, index=chart_days)
    st.line_chart(data)

    st.divider()
    st.subheader("🧠 Nexus AI Assistant")
    st.chat_message("assistant").write(f"Hello {u_name}. How can I help you today?")
    query = st.text_input("Ask a question...")
    if query:
        st.info("🤖 **Assistant:** I recommend 20 mins of mobility work and increasing your hydration.")
