import streamlit as st

def render_workout_tab(u_goal, u_level, i_mod):
    st.title(f"🚀 {u_level} Session")
    st.write(f"Focus: {u_goal}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Strength")
        st.checkbox("Warmup: 10m Dynamic Stretching")
        st.checkbox("Main: 5x5 Compound Movement")
    with col2:
        st.subheader("Conditioning")
        st.checkbox("20m Zone 4 Intervals")
        st.checkbox("Cool down: 5m Breathwork")
