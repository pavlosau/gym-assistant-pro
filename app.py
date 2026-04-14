import streamlit as st
import datetime
import pandas as pd
import numpy as np

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Nexus Hybrid OS", layout="centered", page_icon="⚡")

# --- 2. THE DATABASE SIMULATION (Logic for Login/Trial) ---
# In a real app, this data lives in Supabase.
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

def login_user(email, password):
    # This is where you'd check Supabase. For now, we use a demo:
    if email == "demo@gym.com" and password == "1234":
        st.session_state.logged_in = True
        st.session_state.user_data = {
            "name": "Alex",
            "weight": 85,
            "goal": "Hyrox Pro",
            "trial_start": datetime.date.today() - datetime.timedelta(days=2), # 2 days ago
            "is_paid": False
        }
        return True
    return False

# --- 3. LOGIN / SIGNUP SCREEN ---
if not st.session_state.logged_in:
    st.title("⚡ Nexus Hybrid OS")
    st.subheader("Login to your Training Portal")
    
    auth_tab1, auth_tab2 = st.tabs(["Login", "Create Account (7-Day Trial)"])
    
    with auth_tab1:
        email = st.text_input("Email")
        pw = st.text_input("Password", type="password")
        if st.button("Access Portal"):
            if login_user(email, pw):
                st.rerun()
            else:
                st.error("Invalid credentials. Try demo@gym.com / 1234")
                
    with auth_tab2:
        st.write("Start your 7-day full access trial.")
        new_name = st.text_input("Full Name")
        new_email = st.text_input("New Email")
        if st.button("Start Free Trial"):
            st.success("Account created! Check your email to verify. (Mock)")

else:
    # --- 4. THE AUTHENTICATED APP ---
    user = st.session_state.user_data
    
    # Check Trial Status
    trial_days_used = (datetime.date.today() - user['trial_start']).days
    is_expired = trial_days_used > 7 and not user['is_paid']

    if is_expired:
        st.warning("🚨 Your 7-Day Trial has Expired")
        st.title("Choose a Plan to Continue")
        col1, col2 = st.columns(2)
        with col1:
            st.info("### Individual\n$15/mo\n- Full AI Assistant\n- Hybrid Plans")
            st.button("Pay with Stripe")
        with col2:
            st.info("### Gym Member\nFree via Gym\n- Link your local gym")
            st.button("Enter Gym Code")
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
            
    else:
        # --- 5. THE FULL APP (Personalized) ---
        st.sidebar.success(f"Trial Day {trial_days_used}/7")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

        st.title(f"Welcome Back, {user['name']}")
        st.write(f"Your Goal: **{user['goal']}** | Weight: **{user['weight']}kg**")
        
        tabs = st.tabs(["📅 Your Plan", "📊 Stats", "💳 Subscription"])
        
        with tabs[0]:
            st.subheader(f"Personalized {user['goal']} Session")
            if "Hyrox" in user['goal']:
                st.checkbox("Sled Push: 4x20m @ 125kg")
                st.checkbox("1km Run (Interval)")
            else:
                st.checkbox("12km Base Run")
        
        with tabs[1]:
            st.write("### Your Progress")
            st.line_chart(np.random.randn(10,1))
            
        with tabs[2]:
            st.write("### Billing")
            if not user['is_paid']:
                st.write(f"You have {7 - trial_days_used} days left in your trial.")
                if st.button("Upgrade to Premium"):
                    st.balloons()
