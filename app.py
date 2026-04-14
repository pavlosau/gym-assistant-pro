import streamlit as st
import datetime
import pandas as pd
import numpy as np

# --- 1. INITIALIZATION & AUTH LOGIC ---
st.set_page_config(page_title="Nexus Hybrid OS", layout="centered", page_icon="⚡")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

# Mock Database Function
def attempt_login(email, password):
    # This simulates a user record from a database
    if email == "trainer@gym.com" and password == "nexus123":
        st.session_state.user_data = {
            "name": "Alex",
            "trial_start": datetime.date.today() - datetime.timedelta(days=2), # Joined 2 days ago
            "is_paid": False,
            "gym_access": "Iron Forge Gym"
        }
        st.session_state.logged_in = True
        return True
    return False

# --- 2. GATEKEEPER: LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("⚡ Nexus Hybrid OS")
    st.markdown("### Athlete Authentication")
    
    login_tab, signup_tab = st.tabs(["Member Login", "New Athlete (7-Day Trial)"])
    
    with login_tab:
        email = st.text_input("Email")
        pw = st.text_input("Password", type="password")
        if st.button("Access My Plan"):
            if attempt_login(email, pw):
                st.rerun()
            else:
                st.error("Invalid Login. Use: trainer@gym.com / nexus123")
                
    with signup_tab:
        st.write("Get 7 days of personalized AI coaching.")
        st.text_input("Full Name")
        st.text_input("Preferred Email")
        if st.button("Start Free Trial"):
            st.info("Registration successful! Use the Login tab with the demo credentials.")

else:
    # --- 3. TRIAL VALIDATION ---
    user = st.session_state.user_data
    days_used = (datetime.date.today() - user['trial_start']).days
    
    if days_used > 7 and not user['is_paid']:
        st.error("🚨 Trial Expired")
        st.subheader("Upgrade to Premium to continue your plan")
        st.button("Pay $15/mo via Stripe")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        # --- 4. THE FULL "ULTRA EDITION" APP ---
        
        # --- BRANDING & TENANCY ---
        PARTNERS = {
            "Nexus Individual": {"color": "#00E5FF", "bg": "#001214", "logo": "💠"},
            "Iron Forge Gym": {"color": "#FF3D00", "bg": "#120500", "logo": "⚒️"},
            "Zenith Athletics": {"color": "#7C4DFF", "bg": "#090014", "logo": "🏔️"},
            "Carbon Performance": {"color": "#00E676", "bg": "#000D05", "logo": "🔌"}
        }
        
        # Determine Gym from User Data or Sidebar
        st.sidebar.header("🛡️ Active Portal")
        gym_choice = st.sidebar.selectbox("Partner Portal", list(PARTNERS.keys()), index=1)
        brand = PARTNERS[gym_choice]

        # --- PREMIUM UI STYLING ---
        st.markdown(f"""
            <style>
            .stApp {{ background-color: #050505; color: #E0E0E0; }}
            [data-testid="stMetricValue"] {{ color: {brand['color']}; font-family: 'Inter', sans-serif; font-weight: 800; }}
            .stButton>button {{ 
                background: linear-gradient(90deg, {brand['color']} 0%, {brand['bg']} 100%); 
                color: white; border: 1px solid {brand['color']}; border-radius: 12px; height: 3.8rem;
                font-size: 1.1rem; letter-spacing: 1px; transition: 0.5s;
            }}
            div[data-testid="stExpander"] {{ border: 1px solid #222; border-radius: 12px; background: #0F0F0F; padding: 10px; }}
            .stProgress > div > div > div > div {{ background-color: {brand['color']}; }}
            </style>
            """, unsafe_allow_html=True)

        # --- ATHLETE SIDEBAR ---
        st.sidebar.divider()
        st.sidebar.success(f"Account: {user['name']} (Trial Day {days_used}/7)")
        u_weight = st.sidebar.number_input("Mass (kg)", 40, 160, 85)
        u_goal = st.sidebar.selectbox("Event", ["Hyrox Pro", "Hyrox Open", "Marathon", "Half-Marathon"])
        u_level = st.sidebar.select_slider("Intensity Level", ["Active Recovery", "Foundation", "Performance", "Elite"])
        days_to_race = st.sidebar.number_input("Days to Event", 1, 365, 60)
        
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

        intensity_mod = {"Active Recovery": 0.7, "Foundation": 0.9, "Performance": 1.1, "Elite": 1.3}[u_level]

        # --- MAIN DASHBOARD ---
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            st.title(f"{brand['logo']} {gym_choice}")
            st.write(f"Welcome back, {user['name']}")
        with col_h2:
            st.metric("Countdown", f"{days_to_race}d")

        tabs = st.tabs(["🚀 DAILY WORKOUT", "🥗 PRECISION FUEL", "📊 ANALYTICS", "🧠 AI COACH"])

        # --- TAB 1: WORKOUTS ---
        with tabs[0]:
            st.subheader("Targeted Session")
            with st.expander("⚠️ Pre-Workout Health Check"):
                soreness = st.slider("Muscle Soreness (1-10)", 1, 10, 3)
                if soreness > 7:
                    st.error("High fatigue detected. Today's weights reduced for safety.")
                    intensity_mod *= 0.8

            if "Hyrox" in u_goal:
                base_sled = 175 if "Pro" in u_goal else 125
                st.markdown(f"#### **Hybrid Engine: {u_level} Protocol**")
                c1, c2 = st.columns(2)
                with c1:
                    st.info("Power / Strength")
                    st.checkbox(f"Sled Push: 4x20m @ {int(base_sled * intensity_mod)}kg")
                    st.checkbox(f"Kettlebell Lunges: 100m @ {int(24 * intensity_mod)}kg")
                with c2:
                    st.info("Aerobic Interfacing")
                    st.checkbox(f"Interval Run: 4 x 1km @ {(5.0 - (intensity_mod * 0.5)):.2f} min/km")
                    st.checkbox("Ski-Erg: 1000m")

            elif "Marathon" in u_goal:
                dist = (12 if days_to_race > 14 else 5) * intensity_mod
                st.markdown(f"#### **Endurance Base: Zone 2 Focus**")
                st.checkbox(f"Long Run: {dist:.1f} km")
                st.checkbox("Drills: A-Skips & B-Skips")
            
            if st.button("LOG SESSION AS COMPLETE"):
                st.balloons()
                st.success("Session saved!")

        # --- TAB 2: NUTRITION ---
        with tabs[1]:
            st.subheader("Metabolic Tracking")
            bmr = (10 * u_weight) + 900
            daily_cal = int(bmr * (1.3 if soreness < 5 else 1.1) * intensity_mod)
            nc1, nc2, nc3 = st.columns(3)
            nc1.metric("Calories", f"{daily_cal}")
            nc2.metric("Protein", f"{int(u_weight * 2.2)}g")
            nc3.metric("Carbs", f"{int((daily_cal * 0.55)/4)}g")

        # --- TAB 3: ANALYTICS ---
        with tabs[2]:
            st.subheader("The Lab: Data Trends")
            chart_days = pd.date_range(end=datetime.date.today(), periods=20)
            perf_data = pd.DataFrame({
                "VO2 Max Estimate": np.linspace(45, 52, 20) + np.random.randn(20) * 0.5,
                "Strength Index": np.linspace(100, 140, 20) + np.random.randn(20) * 2
            }, index=chart_days)
            st.line_chart(perf_data)

        # --- TAB 4: AI COACH ---
        with tabs[3]:
            st.subheader("Nexus AI Assistant")
            st.chat_message("assistant").write(f"Hello {user['name']}. I am monitoring your {u_goal} progress.")
            query = st.text_input("Ask a recovery question...")
            if query:
                st.warning("Recommendation: Focus on eccentric movements and infra-red therapy.")

        st.markdown("---")
        st.caption(f"© 2026 Nexus Hybrid OS | v2.0.4 Premium | {user['name']}'s Portal")
