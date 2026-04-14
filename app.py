import streamlit as st
import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Gym Assistant AI", layout="centered")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #FF4B4B; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: User Profile ---
st.sidebar.header("👤 User Profile")
weight = st.sidebar.number_input("Weight (kg)", value=80.0)
height = st.sidebar.number_input("Height (cm)", value=180.0)
age = st.sidebar.number_input("Age", value=25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
goal = st.sidebar.selectbox("Training Goal", ["Hyrox Prep", "Marathon Prep", "Half-Marathon"])

# --- CALCULATIONS ---
# BMR Calculation (Mifflin-St Jeor)
s = 5 if gender == "Male" else -161
bmr = (10 * weight) + (6.25 * height) - (5 * age) + s

# --- MAIN UI ---
st.title("🚀 Gym Assistant Pro")
st.subheader(f"Target: {goal}")

tabs = st.tabs(["📅 Daily Workout", "🥗 Nutrition AI", "📊 Progress"])

with tabs[0]:
    st.write(f"### Today's {goal} Session")
    
    if goal == "Hyrox Prep":
        st.info("Focus: Strength-Endurance Interfacing")
        st.checkbox("1km Warmup Run")
        st.checkbox(f"Sled Push: 4 x 20m @ {weight * 1.5}kg")
        st.checkbox("800m Run (Fast)")
        st.checkbox("Burpee Broad Jumps: 80m")
        st.checkbox("1km Cool down")
        
    elif "Marathon" in goal:
        st.info("Focus: Aerobic Base & Zone 2")
        st.checkbox("10km Easy Run (Heart Rate < 145bpm)")
        st.checkbox("Core: 3 Rounds of Planks and Deadbugs")
        st.write("**Tip:** Focus on cadence (170-180 spm).")

with tabs[1]:
    st.write("### Personalized Macros")
    activity_level = st.select_slider("Today's Activity Level", options=["Rest", "Moderate", "Elite Training"])
    
    multipliers = {"Rest": 1.2, "Moderate": 1.5, "Elite Training": 1.9}
    tdee = bmr * multipliers[activity_level]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Calories", f"{int(tdee)} kcal")
    col2.metric("Protein", f"{int(weight * 2)}g")
    col3.metric("Carbs", f"{int((tdee * 0.5)/4)}g")
    
    st.progress(0.7, text="Carbohydrate Loading Status")

with tabs[2]:
    st.write("### Gym Owner Dashboard View")
    st.line_chart([weight - 2, weight - 1.5, weight - 1, weight])
    st.success(f"Goal Projection: On track for {goal} in 12 weeks!")
