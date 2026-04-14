import streamlit as st

def render_workout_tab(u_goal, u_level, intensity_mod, days_to_race):
    st.subheader("Your Personalized Session")
    with st.expander("⚠️ Daily Health Check"):
        soreness = st.slider("Muscle Soreness (1-10)", 1, 10, 3)
        if soreness > 7:
            st.error("Extreme Fatigue Detected. Power outputs reduced.")
            intensity_mod *= 0.8

    if "Hyrox" in u_goal:
        base_sled = 175 if "Pro" in u_goal else 125
        st.markdown(f"#### **Hybrid Protocol: {u_level}**")
        c1, c2 = st.columns(2)
        with c1:
            st.info("Power / Functional")
            st.checkbox(f"Sled Push: 4x20m @ {int(base_sled * intensity_mod)}kg")
            st.checkbox(f"Sandbag Lunges: 100m @ {int(30 * intensity_mod)}kg")
        with c2:
            st.info("Engine / Aerobic")
            st.checkbox(f"Run: 1km @ {(5.0 - (intensity_mod * 0.5)):.2f} min/km")
            st.checkbox("Row: 1000m")
    
    elif "Marathon" in u_goal:
        dist = (15 if days_to_race > 14 else 6) * intensity_mod
        st.markdown(f"#### **Aerobic Base: Zone 2 Focus**")
        st.checkbox(f"Endurance Run: {dist:.1f} km")
        st.checkbox("Drills: 3x100m High Knees")

    if st.button("SUBMIT WORKOUT"):
        st.balloons()
        st.success("Session saved!")
