import streamlit as st
import random

# --- 1. MEAL DATABASE ---
FOOD_DB = {
    "Hyrox_Breakfast": ["Egg White Omelet & Avocado", "Protein Pancakes", "Steak & Eggs", "Greek Yogurt & Nut Butter"],
    "Hyrox_Lunch": ["Grilled Chicken & Quinoa", "Lean Beef Bowl", "Turkey Meatballs & Pasta", "Tuna Salad & Rice Cakes"],
    "Hyrox_Dinner": ["Baked Salmon & Greens", "Stir-fry Lean Beef", "Cod & Sweet Potato", "Chicken Breast & Asparagus"],
    "Endurance_Breakfast": ["Oatmeal & Banana", "Bagel & Peanut Butter", "Cream of Rice & Berries", "Smoothie Bowl"],
    "Endurance_Lunch": ["Pasta Carbonara (Lean)", "Rice & Beans Bowl", "Chicken Wrap", "Potato Salad & Ham"],
    "Endurance_Dinner": ["Spaghetti Bolognese", "Baked Potato & Tuna", "Risotto & Veggies", "Chicken Paella"]
}

# --- 2. LOGIC ENGINES ---
def generate_weekly_plan(goal):
    """Creates a full 7-day dictionary of meals based on the athlete's goal."""
    category = "Hyrox" if "Hyrox" in goal else "Endurance"
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    plan = {}
    for day in days:
        plan[day] = {
            "Breakfast": random.choice(FOOD_DB[f"{category}_Breakfast"]),
            "Lunch": random.choice(FOOD_DB[f"{category}_Lunch"]),
            "Dinner": random.choice(FOOD_DB[f"{category}_Dinner"])
        }
    return plan

def refresh_meal(day, meal_type, goal):
    """Swaps a specific meal for a different one in the same category."""
    category = "Hyrox" if "Hyrox" in goal else "Endurance"
    current_meal = st.session_state.weekly_meals[day][meal_type]
    
    # Get all options except the one currently selected
    options = [f for f in FOOD_DB[f"{category}_{meal_type}"] if f != current_meal]
    st.session_state.weekly_meals[day][meal_type] = random.choice(options)

# --- 3. THE VISUAL INTERFACE ---
def render_nutrition_tab(u_name, u_goal, u_weight, intensity_mod):
    st.title("🍎 AI Nutritionist")
    
    # Macro Calculations
    prot_ratio = 2.2 if "Hyrox" in u_goal else 1.8
    bmr = (10 * u_weight) + 900
    tdee = int(bmr * 1.5 * intensity_mod)
    
    prot_g = int(u_weight * prot_ratio)
    carb_g = int((tdee * 0.55) / 4) if "Marathon" in u_goal else int((tdee * 0.40) / 4)

    # Top Metrics Row
    st.markdown(f"### Nutrient Strategy for {u_name}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Daily Target", f"{tdee} kcal")
    col2.metric("Protein", f"{prot_g}g")
    col3.metric("Carbohydrates", f"{carb_g}g")

    st.divider()
    
    # Weekly Grid Section
    st.subheader("🍴 7-Day Precision Meal Plan")
    st.caption("Don't like a meal? Click the 🔄 button to swap it for a similar alternative.")
    
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    grid_cols = st.columns(7)
    
    for i,
