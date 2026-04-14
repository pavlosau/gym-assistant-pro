import streamlit as st
import pandas as pd
import numpy as np

def render_analytics_tab():
    st.title("📊 Performance Lab")
    st.line_chart(pd.DataFrame(np.random.randn(20, 3), columns=['Speed', 'Power', 'Recovery']))
    st.metric("VO2 Max Estimate", "54.2", "+1.2")
