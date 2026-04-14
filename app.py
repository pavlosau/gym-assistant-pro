import streamlit as st
import datetime
import pandas as pd
import numpy as np

# --- 1. INITIALIZATION & AUTHENTICATION LOGIC ---
st.set_page_config(page_title="Nexus Hybrid OS", layout="centered", page_icon="⚡")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None

def check_login(email, password):
    # This simulates a database record. 
    # Logic: User joined 2 days ago, trial is active.
    if email == "user@test.com" and password == "1234":
        st.session_state.user_profile = {
            "name": "Alex",
            "trial_start": datetime.date.today() - datetime.timedelta(days=2),
            "is_paid": False
        }
        st.session_state.logged_in = True
        return True
    return False

# --- 2. THE LOGIN & TRIAL GATEKEEPER ---
if not st.session_state.logged_in:
    st.title("⚡ Nexus Hybrid OS")
    st.markdown("### Athlete Portal Login")
    
    auth_tab1, auth_tab2 = st.tabs(["Member Login", "Start 7-Day Free Trial"])
    
    with auth_tab1:
        email_in = st.text_input("Email")
        pass_in = st.text_input("Password", type="password")
        if st.button("Access My Plan"):
            if check_login(email_in, pass_in):
                st.rerun()
            else:
                st.error("Invalid credentials. Try: user@test.com / 1234")
    
    with auth_tab2:
        st.write("Join the elite. Your 7-day trial starts immediately.")
        st.text_input("Full Name")
        st.text_input("Preferred Email")
        if st.button("Sign Up Now"):
            st.success("Registration successful! Please log in with the demo account.")

else:
    # --- 3. TRIAL VALIDATION ---
    user = st.session_state.user_profile
    days_used = (datetime.date.today() - user['trial_start']).days
    
    if days_used > 7 and not user['is_paid']:
        st.error("🚨 Access Restricted: Trial Expired")
        st.subheader("Your 7-day trial has concluded.")
        st.write("Upgrade to a premium membership to unlock your saved plans and history.")
        st.button("Upgrade to Premium ($15/mo)")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        # --- 4. THE COMPLETE "ULTRA" DASHBOARD ---
        
        # Multi-Tenant Gym Branding
        PARTNERS = {
            "Nexus Elite": {"color": "#00E5FF", "bg": "#001214", "logo": "💠"},
            "Iron Forge Gym": {"color": "#FF3D00", "bg": "#120500", "logo": "⚒️"},
            "Zenith Athletics": {"color": "#7C4DFF", "bg": "#090014", "logo": "🏔️"},
            "Carbon Performance": {"color": "#00E676", "bg": "#000D05", "logo": "🔌"}
        }

        st.sidebar.header("🛡️ Partner Portal")
        gym_choice = st.sidebar.selectbox("Active Portal", list(PARTNERS.keys()))
        brand = PARTNERS[gym_choice]

        # Premium Professional UI Styling
        st.markdown(f"""
            <style>
            .stApp {{ background-color: #050505; color: #E0E0E0; }}
            [data-testid="stMetricValue"] {{ color: {brand['color']}; font-family: 'Inter', sans-serif; font-weight: 800; }}
            .stButton>button {{ 
                background: linear-gradient(90deg, {brand['color']} 0%, {brand['bg']} 100%); 
                color: white; border: 1px solid {brand['color']}; border-radius: 12px; height: 3.8rem;
                font-size: 1.1rem; letter-spacing: 1px; transition: 0.5s;
            }}
            .stButton>button:hover {{ box-shadow: 0px 0px 15px {brand['color']}; transform: scale(1.02); }}
            div.stBlock {{ border: 1px solid #222; border-radius: 12px; background: #0F0F0F; padding: 20px; }}
            div[data-testid="stExpander"] {{ border: 1px solid #222; border-radius: 12px; background: #0F0F0F; }}
            .stProgress > div > div > div > div {{ background-color: {brand['color']}; }}
            </style>
            """, unsafe_allow_html=True)

        # Athlete Personalization Sidebar
        st.sidebar.divider()
        st.sidebar.subheader("Athlete Intelligence")
        st.sidebar.success(f"Trial Day {days_used}/7")
        u_name = st.sidebar.text_input("Athlete Name", user['name'])
        u_weight = st.sidebar.number_input("Mass (kg)", 40, 160, 85)
        u_goal = st.sidebar.selectbox("Event Goal", ["Hyrox Pro", "Hyrox Open", "Marathon", "Half-Marathon"])
        u_level = st.sidebar.select_slider("Intensity Level", ["Active Recovery", "Foundation", "Performance", "Elite"])
        days_to_race = st.sidebar.number_input("Days to Event", 1, 365, 45)
        
        if st.sidebar.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()

        intensity_mod = {"Active Recovery": 0.7, "Foundation": 0.9, "Performance": 1.1, "Elite": 1.3}[u_level]

        # Header Section
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            st.title(f"{brand['logo']} {gym_choice}")
            st.write(f"**Welcome, {u_name}**")
        with col_h2:
            st.metric("Countdown", f"{days_to_race}d")

        tabs = st.tabs(["🚀 DYNAMIC WORKOUT", "🥗 NUTRITION COACH", "📊 DATA LAB", "🧠 AI ASSISTANT"])

        # --- TAB 1: DYNAMIC WORKOUT ENGINE ---
        with tabs[0]:
            st.subheader("Your Personalized Session")
            with st.expander("⚠️ Daily Health Check"):
                soreness = st.slider("Muscle Soreness (1-10)", 1, 10, 3)
                if soreness > 7:
                    st.error("Extreme Fatigue Detected. Power outputs reduced for injury prevention.")
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
                    st.checkbox("Row: 1000m (Target Pace)")
            
            elif "Marathon" in u_goal:
                dist = (15 if days_to_race > 14 else 6) * intensity_mod
                st.markdown(f"#### **Aerobic Base: Zone 2 Focus**")
                st.checkbox(f"Endurance Run: {dist:.1f} km")
                st.checkbox("Drills: 3x100m High Knees & Butt Kicks")

            if st.button("SUBMIT WORKOUT"):
                st.balloons()
                st.success("Session saved to Gym Dashboard!")

        # --- TAB 2: PERSONALIZED NUTRITION COACH ---
        with tabs[1]:
            st.title("🍎 AI Nutritionist")
            
            # Logic: Protein 2.2g/kg for strength goals, 1.8g/kg for endurance
            prot_ratio = 2.2 if "Hyrox" in u_goal else 1.8
            bmr = (10 * u_weight) + 900
            tdee = int(bmr * 1.5 * intensity_mod)
            
            prot_g = int(u_weight * prot_ratio)
            carb_g = int((tdee * 0.55) / 4) if "Marathon" in u_goal else int((tdee * 0.40) / 4)
            fat_g = int((tdee - (prot_g * 4) - (carb_g * 4)) / 9)

            st.write(f"### Nutrient Strategy: {'Muscle Repair' if 'Hyrox' in u_goal else 'Glycogen Saturation'}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Calories", f"{tdee}")
            col2.metric("Protein (g)", f"{prot_g}")
            col3.metric("Carbs (g)", f"{carb_g}")

            st.divider()
            st.subheader("🍴 Tailored Meal Plan")
            
            if "Hyrox" in u_goal:
                meals = {
                    "Breakfast": "Egg White Omelet + Turkey Bacon + Avocado",
                    "Lunch": "Grilled Chicken, Sweet Potato, Spinach",
                    "Snack": "Greek Yogurt + 30g Almonds",
                    "Dinner": "Steak Stir-fry with Peppers and Brown Rice"
                }
            else:
                meals = {
                    "Breakfast": "Oatmeal with Honey, Banana, and Chia Seeds",
                    "Lunch": "Salmon Fillet with Large Portion of Wholewheat Pasta",
                    "Snack": "Rice Cakes with Peanut Butter and Jam",
                    "Dinner": "Baked Turkey, Baked Potatoes, and Steamed Greens"
                }

            for meal, detail in meals.items():
                with st.container():
                    st.markdown(f"**{meal}**")
                    st.caption(detail)
            
            st.info(f"💡 **Nutritionist Note:** To optimize performance, aim for {int(u_weight * 35)}ml of water today.")

        # --- TAB 3: PERFORMANCE DATA LAB ---
        with tabs[2]:
            st.subheader("Data Trend Analysis")
            chart_days = pd.date_range(end=datetime.date.today(), periods=15)
            data = pd.DataFrame({
                "Performance Index": np.linspace(60, 92, 15) + np.random.randn(15) * 3,
                "Recovery Score": np.random.randint(40, 95, 15)
            }, index=chart_days)
            st.line_chart(data)

        # --- TAB 4: AI ASSISTANT ---
        with tabs[3]:
            st.subheader("Nexus AI Assistant")
            st.chat_message("assistant").write(f"Hello {u_name}. Your stats show you are {days_to_race} days from your {u_goal} race. How can I help you today?")
            query = st.text_input("Describe your feeling or ask a question...")
            if query:
                with st.spinner("Analyzing bio-metrics..."):
                    st.write("🤖 **Assistant:** Based on your current load, I recommend 20 mins of foam rolling and increasing your sleep by 1 hour tonight to avoid CNS fatigue.")

        st.markdown("---")
        st.caption(f"© 2026 Nexus Hybrid OS | Licensed to {gym_choice} | v3.0.1 Enterprise")        if st.button("Access My Plan"):
            if check_login(email_in, pass_in):
                st.rerun()
            else:
                st.error("Invalid credentials. Try: user@test.com / 1234")
    
    with auth_tab2:
        st.write("Join the elite. Your 7-day trial starts immediately.")
        st.text_input("Full Name")
        st.text_input("Preferred Email")
        if st.button("Sign Up Now"):
            st.success("Registration successful! Please log in with the demo account.")

else:
    # --- 3. TRIAL VALIDATION ---
    user = st.session_state.user_profile
    days_used = (datetime.date.today() - user['trial_start']).days
    
    if days_used > 7 and not user['is_paid']:
        st.error("🚨 Access Restricted: Trial Expired")
        st.subheader("Your 7-day trial has concluded.")
        st.write("Upgrade to a premium membership to unlock your saved plans and history.")
        st.button("Upgrade to Premium ($15/mo)")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        # --- 4. THE COMPLETE "ULTRA" DASHBOARD ---
        
        # Multi-Tenant Gym Branding
        PARTNERS = {
            "Nexus Elite": {"color": "#00E5FF", "bg": "#001214", "logo": "💠"},
            "Iron Forge Gym": {"color": "#FF3D00", "bg": "#120500", "logo": "⚒️"},
            "Zenith Athletics": {"color": "#7C4DFF", "bg": "#090014", "logo": "🏔️"},
            "Carbon Performance": {"color": "#00E676", "bg": "#000D05", "logo": "🔌"}
        }

        st.sidebar.header("🛡️ Partner Portal")
        gym_choice = st.sidebar.selectbox("Active Portal", list(PARTNERS.keys()))
        brand = PARTNERS[gym_choice]

        # Premium Professional UI Styling
        st.markdown(f"""
            <style>
            .stApp {{ background-color: #050505; color: #E0E0E0; }}
            [data-testid="stMetricValue"] {{ color: {brand['color']}; font-family: 'Inter', sans-serif; font-weight: 800; }}
            .stButton>button {{ 
                background: linear-gradient(90deg, {brand['color']} 0%, {brand['bg']} 100%); 
                color: white; border: 1px solid {brand['color']}; border-radius: 12px; height: 3.8rem;
                font-size: 1.1rem; letter-spacing: 1px; transition: 0.5s;
            }}
            .stButton>button:hover {{ box-shadow: 0px 0px 15px {brand['color']}; transform: scale(1.02); }}
            div.stBlock {{ border: 1px solid #222; border-radius: 12px; background: #0F0F0F; padding: 20px; }}
            div[data-testid="stExpander"] {{ border: 1px solid #222; border-radius: 12px; background: #0F0F0F; }}
            .stProgress > div > div > div > div {{ background-color: {brand['color']}; }}
            </style>
            """, unsafe_allow_html=True)

        # Athlete Personalization Sidebar
        st.sidebar.divider()
        st.sidebar.subheader("Athlete Intelligence")
        st.sidebar.success(f"Trial Day {days_used}/7")
        u_name = st.sidebar.text_input("Athlete Name", user['name'])
        u_weight = st.sidebar.number_input("Mass (kg)", 40, 160, 85)
        u_goal = st.sidebar.selectbox("Event Goal", ["Hyrox Pro", "Hyrox Open", "Marathon", "Half-Marathon"])
        u_level = st.sidebar.select_slider("Intensity Level", ["Active Recovery", "Foundation", "Performance", "Elite"])
        days_to_race = st.sidebar.number_input("Days to Event", 1, 365, 45)
        
        if st.sidebar.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()

        intensity_mod = {"Active Recovery": 0.7, "Foundation": 0.9, "Performance": 1.1, "Elite": 1.3}[u_level]

        # Header Section
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            st.title(f"{brand['logo']} {gym_choice}")
            st.write(f"**Welcome, {u_name}**")
        with col_h2:
            st.metric("Countdown", f"{days_to_race}d")

        tabs = st.tabs(["🚀 DYNAMIC WORKOUT", "🥗 NUTRITION COACH", "📊 DATA LAB", "🧠 AI ASSISTANT"])

        # --- TAB 1: DYNAMIC WORKOUT ENGINE ---
        with tabs[0]:
            st.subheader("Your Personalized Session")
            with st.expander("⚠️ Daily Health Check"):
                soreness = st.slider("Muscle Soreness (1-10)", 1, 10, 3)
                if soreness > 7:
                    st.error("Extreme Fatigue Detected. Power outputs reduced for injury prevention.")
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
                    st.checkbox("Row: 1000m (Target Pace)")
            
            elif "Marathon" in u_goal:
                dist = (15 if days_to_race > 14 else 6) * intensity_mod
                st.markdown(f"#### **Aerobic Base: Zone 2 Focus**")
                st.checkbox(f"Endurance Run: {dist:.1f} km")
                st.checkbox("Drills: 3x100m High Knees & Butt Kicks")

            if st.button("SUBMIT WORKOUT"):
                st.balloons()
                st.success("Session saved to Gym Dashboard!")

        # --- TAB 2: PERSONALIZED NUTRITION COACH ---
        with tabs[1]:
            st.title("🍎 AI Nutritionist")
            
            # Logic: Protein 2.2g/kg for strength goals, 1.8g/kg for endurance
            prot_ratio = 2.2 if "Hyrox" in u_goal else 1.8
            bmr = (10 * u_weight) + 900
            tdee = int(bmr * 1.5 * intensity_mod)
            
            prot_g = int(u_weight * prot_ratio)
            carb_g = int((tdee * 0.55) / 4) if "Marathon" in u_goal else int((tdee * 0.40) / 4)
            fat_g = int((tdee - (prot_g * 4) - (carb_g * 4)) / 9)

            st.write(f"### Nutrient Strategy: {'Muscle Repair' if 'Hyrox' in u_goal else 'Glycogen Saturation'}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Calories", f"{tdee}")
            col2.metric("Protein (g)", f"{prot_g}")
            col3.metric("Carbs (g)", f"{carb_g}")

            st.divider()
            st.subheader("🍴 Tailored Meal Plan")
            
            if "Hyrox" in u_goal:
                meals = {
                    "Breakfast": "Egg White Omelet + Turkey Bacon + Avocado",
                    "Lunch": "Grilled Chicken, Sweet Potato, Spinach",
                    "Snack": "Greek Yogurt + 30g Almonds",
                    "Dinner": "Steak Stir-fry with Peppers and Brown Rice"
                }
            else:
                meals = {
                    "Breakfast": "Oatmeal with Honey, Banana, and Chia Seeds",
                    "Lunch": "Salmon Fillet with Large Portion of Wholewheat Pasta",
                    "Snack": "Rice Cakes with Peanut Butter and Jam",
                    "Dinner": "Baked Turkey, Baked Potatoes, and Steamed Greens"
                }

            for meal, detail in meals.items():
                with st.container():
                    st.markdown(f"**{meal}**")
                    st.caption(detail)
            
            st.info(f"💡 **Nutritionist Note:** To optimize performance, aim for {int(u_weight * 35)}ml of water today.")

        # --- TAB 3: PERFORMANCE DATA LAB ---
        with tabs[2]:
            st.subheader("Data Trend Analysis")
            chart_days = pd.date_range(end=datetime.date.today(), periods=15)
            data = pd.DataFrame({
                "Performance Index": np.linspace(60, 92, 15) + np.random.randn(15) * 3,
                "Recovery Score": np.random.randint(40, 95, 15)
            }, index=chart_days)
            st.line_chart(data)

        # --- TAB 4: AI ASSISTANT ---
        with tabs[3]:
            st.subheader("Nexus AI Assistant")
            st.chat_message("assistant").write(f"Hello {u_name}. Your stats show you are {days_to_race} days from your {u_goal} race. How can I help you today?")
            query = st.text_input("Describe your feeling or ask a question...")
            if query:
                with st.spinner("Analyzing bio-metrics..."):
                    st.write("🤖 **Assistant:** Based on your current load, I recommend 20 mins of foam rolling and increasing your sleep by 1 hour tonight to avoid CNS fatigue.")

        st.markdown("---")
        st.caption(f"© 2026 Nexus Hybrid OS | Licensed to {gym_choice} | v3.0.1 Enterprise")
