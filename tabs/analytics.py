import streamlit as st
import pandas as pd
import numpy as np

def render_analytics_tab():
    st.title("📊 Performance Analytics")
    
    # Mock Performance Data
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Strength', 'Endurance', 'Recovery']
    )
    st.area_chart(chart_data)
    
    col1, col2 = st.columns(2)
    col1.metric("VO2 Max", "54.2", "+2.1")
    col2.metric("Weekly Load", "450 TSS", "-10%")
