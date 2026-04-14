import streamlit as st
import datetime
import pandas as pd
import numpy as np

# --- 1. SETTINGS & BRANDING ---
# st.set_page_config MUST be the first streamlit command
st.set_page_config(page_title="Hybrid Athlete Pro", layout="centered", page_icon="💪")

# Dictionary of Gym Partners - This is your B2B selling point!
gym_configs = {
    "Individual Subscriber": {"color": "#FF4B4B", "logo": "👤"},
    "Iron Paradise Gym": {"color": "#1E90FF", "logo": "🏋️‍♂️"},
    "Elite Endurance Hub": {"color": "#32CD32", "logo": "🏃‍♂️"},
    "Metabolic CrossFit": {"color": "#FFD700", "logo": "🔥"}
}

# Sidebar for Setup
st.sidebar.header("🏢 Portal Settings")
selected_gym = st.sidebar.selectbox("Active Portal", list(gym_configs.keys()))
theme_color = gym_configs[selected_gym]["color"]
gym_logo = gym_configs[selected_gym]["logo"]

# Custom CSS to inject gym branding colors
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: white; }}
    .stButton>button {{ 
        width: 100%; border-radius: 12px; 
        background-color: {theme_color}; color: white; border: none;
        font-weight: bold; height: 3em;
    }}
    .stProgress > div > div > div > div {{ background-color: {theme_color}; }}
    [data-testid="stMetricValue"] {{ color: {theme_color}; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. USER DATA INPUT ---
st.sidebar.divider()
st.sidebar.header("👤 Athlete Profile")
user_name = st.sidebar.text_input("Athlete Name", "Alex")
u_weight = st.sidebar.number_input("Weight (kg)", 50, 150, 80)
u_height = st.sidebar.number_input("Height (cm)", 120, 220, 180)
u_goal = st.sidebar.selectbox("Primary Goal", ["Hyrox Prep", "Marathon Prep", "Half-Marathon", "Strength & Conditioning"])

# Nutrition Logic (Mifflin-St Jeor)
bmr = (10 * u_weight) + (6.25 * u_height) - (5 * 25) + 5 # Simplified age/gender for prototype

# --- 3. MAIN INTERFACE ---
st.title(f"{gym_logo} {selected_gym}")
st.header(f"Welcome back, {user_name}!")

tabs = st.tabs(["⚡ Training", "🍎 Nutrition", "📈 Analytics", "🤖 Assistant"])

# TABS 1: TRAINING LOGIC
with tabs[0]:
    date_str = datetime.date.today().strftime("%B %d, %Y")
    st.subheader(f"Session for {date_str}")
    
    if u_goal == "Hyrox Prep":
        st.caption("Focus: Hybrid Strength & Aerobic Capacity")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Strength Block**")
            st.checkbox(f"Sled Push: 4x20m @ {u_weight * 1.5}kg")
            st.checkbox("Wall Balls: 50 Reps (6/9kg)")
        with col2:
            st.write("**Engine Block**")
            st.checkbox("1km Run (Pace: 4:30/km)")
            st.checkbox("500m Row (Sprit)")
            
    elif "Marathon" in u_goal:
        st.caption("Focus: Zone 2 Endurance")
        st.write("**Endurance Block**")
        st.checkbox("8km Easy Run (HR 130-140)")
        st.checkbox("Post-run Mobility (10 mins)")
    
    if st.button("Submit Session"):
        st.balloons()
        st.success("Session saved to Gym Cloud!")

# TAB 2: NUTRITION
with tabs[1]:
    st.subheader("Fueling Plan")
    activity = st.select_slider("Daily Intensity", options=["Rest", "Training", "Race Day"])
    mult = {"Rest": 1.2, "Training": 1.5, "Race Day": 1.9}[activity]
    total_cal = int(bmr * mult)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Target Calories", f"{total_cal} kcal")
    c2.metric("Protein", f"{u_weight * 2}g")
    c3.metric("Carbs", f"{int((total_cal*0.5)/4)}g")
    
    st.progress(0.65, text="Daily Calorie Intake")

# TAB 3: ANALYTICS
with tabs[2]:
    st.subheader("Performance Trends")
    chart_data = pd.DataFrame(
        np.random.randn(10, 2) + [u_weight, 50],
        columns=['Weight', 'Running Volume (km)']
    )
    st.line_chart(chart_data)
    
    col_a, col_b = st.columns(2)
    col_a.metric("Current VO2 Max", "52", "+1.2")
    col_b.metric("Deadlift 1RM", f"{u_weight * 1.8}kg", "+5kg")

# TAB 4: AI ASSISTANT
with tabs[3]:
    st.subheader("Smart Training Assistant")
    st.write("Ask about your training, diet, or recovery.")
    query = st.text_input("Ask me anything...")
    if query:
        with st.spinner('Analyzing data...'):
            st.chat_message("assistant").write(f"Based on your goal of {u_goal}, your current weight of {u_weight}kg, and today's session, I recommend increasing your carb intake by 40g and focusing on sleep tonight. Would you like me to adjust tomorrow's run pace?")
