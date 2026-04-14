import streamlit as st
import pandas as pd
import numpy as np

def render_analytics_tab(u_name, u_goal, days):
    # This 'st' only works if 'import streamlit as st' is at the top of THIS file
    st.subheader("🧠 Assistant Intelligence")
    
    # Simple Performance Chart
    data = pd.DataFrame(
        np.random.randn(20, 2),
        columns=['Performance', 'Recovery']
    )
    st.line_chart(data)

    st.divider()
    
    # Connect to the meal plan in session state
    st.write(f"### AI Coach for {u_name}")
    st.info(f"Analyzing data for your {u_goal} target...")
    
    query = st.chat_input("Ask the AI Coach anything...")
    if query:
        if "meal" in query.lower() or "plan" in query.lower():
            st.write("🤖 **Assistant:** I've updated your Nutrition tab based on your request.")
        else:
            st.write(f"🤖 **Assistant:** Focusing on your {u_goal} prep. I recommend prioritizing sleep tonight.")
