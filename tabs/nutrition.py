import streamlit as st
import random

FOOD_DB = {
    "Hyrox_Breakfast": ["Egg White Omelet & Avocado", "Protein Pancakes", "Steak & Eggs"],
    "Hyrox_Lunch": ["Grilled Chicken & Quinoa", "Lean Beef Bowl", "Turkey Meatballs"],
    "Hyrox_Dinner": ["Baked Salmon & Greens", "Stir-fry Lean Beef", "Cod & Sweet Potato"],
    "Endurance_Breakfast": ["Oatmeal & Banana", "Bagel & Peanut Butter", "Cream of Rice"],
    "Endurance_Lunch": ["Pasta Carbonara", "Rice & Beans Bowl", "Chicken Wrap"],
    "Endurance_Dinner": ["Spaghetti Bolognese", "Baked Potato & Tuna", "Risotto"]
}

def generate_weekly_plan(goal):
    cat = "Hyrox" if "Hyrox" in goal else "Endurance"
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    plan = {}
    for d in days:
        plan[d] = {
            "Breakfast": random.choice(FOOD_DB[f"{cat}_Breakfast"]),
            "Lunch": random.choice(FOOD_DB[f"{cat}_Lunch"]),
            "Dinner": random.choice(FOOD_DB[f"{cat}_Dinner"])
        }
    return plan

def refresh_meal(day, m_type, goal):
    cat = "Hyrox" if "Hyrox" in goal else "Endurance"
    curr = st.session_state.weekly_meals[day][m_type]
    opts = [f for f in FOOD_DB[f"{cat}_{m_type}"] if f != curr]
    st.session_state.weekly_meals[day][m_type] = random.choice(opts)

def render_nutrition_tab(u_name, u_goal, u_weight, i_mod):
    st.title("🍎 AI Nutritionist")
    
    cal = int(((10 * u_weight) + 900) * 1.5 * i_mod)
    prot = int(u_weight * (2.2 if "Hyrox" in u_goal else 1.8))
    
    c1, c2 = st.columns(2)
    c1.metric("Daily Calories", f"{cal} kcal")
    c2.metric("Target Protein", f"{prot} g")

    st.divider()
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cols = st.columns(7)
    
    for i, d in enumerate(days):
        with cols[i]:
            st.markdown(f"**{d}**")
            for mt in ["Breakfast", "Lunch", "Dinner"]:
                st.caption(mt)
                st.write(st.session_state.weekly_meals[d][mt])
                if st.button("🔄", key=f"btn_{d}_{mt}"):
                    refresh_meal(d, mt, u_goal)
                    st.rerun()
            st.write("---")
