import streamlit as st

def render_workout_tab(u_goal, u_level, i_mod):
    st.subheader(f"🚀 Training Phase: {u_level}")
    st.info(f"Targeting: {u_goal}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Strength Block**")
        st.checkbox("Compound Lift (Main Set)")
        st.checkbox("Accessory Movement")
    with col2:
        st.write("**Energy Systems**")
        st.checkbox("Interval Conditioning")
        st.checkbox("Mobility/Cool Down")

    if st.button("Complete Session"):
        st.success("Session Logged!")
