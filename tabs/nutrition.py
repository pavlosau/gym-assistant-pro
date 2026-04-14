import streamlit as st
import random

FOOD_DB = {
    "Hyrox_Breakfast": ["Egg White Omelet & Avocado", "Protein Pancakes", "Steak & Eggs", "Greek Yogurt & Nut Butter"],
    "Hyrox_Lunch": ["Grilled Chicken & Quinoa", "Lean Beef Bowl", "Turkey Meatballs & Pasta", "Tuna Salad & Rice Cakes"],
    "Hyrox_Dinner": ["Baked Salmon & Greens", "Stir-fry Lean Beef", "Cod & Sweet Potato", "Chicken Breast & Asparagus"],
    "Endurance_Breakfast": ["Oatmeal & Banana", "Bagel & Peanut Butter", "Cream of Rice & Berries", "Smoothie Bowl"],
    "Endurance_Lunch": ["Pasta Carbonara (Lean)", "Rice & Beans Bowl", "Chicken Wrap", "Potato Salad & Ham"],
    "Endurance_Dinner": ["Spaghetti Bolognese", "Baked Potato & Tuna", "Risotto & Veggies", "Chicken Paella"]
}

def refresh_meal(day, meal_type, goal):
    category = "Hyrox" if "Hyrox" in goal else "Endurance"
    current_meal = st.session_state.weekly_meals[day][meal_type]
    options = [f for f in FOOD_DB[f"{category}_{meal_type}"] if f != current_meal]
    st.session_state.weekly_meals[day][meal_type] = random.choice(options)

def render_nutrition_tab(u_name, u_goal, u_weight, intensity_mod):
    st.title("🍎 AI Nutritionist")
    
    # Core Logic
    prot_ratio = 2.2 if "Hyrox" in u_goal else 1.8
    bmr = (10 * u_weight) + 900
    tdee = int(bmr * 1.5 * intensity_mod)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Calories", f"{tdee}")
    col2.metric("Protein (g)", f"{int(u_weight * prot_ratio)}")
    col3.metric("Carbs (g)", f"{int((tdee * 0.55) / 4) if 'Marathon' in u_goal else int((tdee * 0.40) / 4)}")

    st.divider()
    st.subheader("🍴 7-Day Precision Meal Plan")
    
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cols = st.columns(7)
    
    for i, day in enumerate(days):
        with cols[i]:
            st.markdown(f"**{day}**")
            for meal in ["Breakfast", "Lunch", "Dinner"]:
                st.caption(f"**{meal}**")
                st.write(st.session_state.weekly_meals[day][meal])
                if st.button("🔄", key=f"ref_{day}_{meal}"):
                    refresh_meal(day, meal, u_goal)
                    st.rerun()
            st.write("---")
