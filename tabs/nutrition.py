def generate_weekly_plan(goal, weight, requirements="None"):
    # We add a "Schema" instruction to force Gemini to use valid JSON
    prompt = f"""
    Create a 7-day meal plan for a {weight}kg athlete training for {goal}.
    DIETARY RESTRICTION: {requirements}

    Return ONLY a valid JSON object. 
    Strictly follow this structure:
    {{
      "Mon": {{"Breakfast": "Meal info", "Lunch": "Meal info", "Dinner": "Meal info"}},
      "Tue": {{...}}, "Wed": {{...}}, "Thu": {{...}}, "Fri": {{...}}, "Sat": {{...}}, "Sun": {{...}}
    }}
    Do not include any text before or after the JSON.
    """
    try:
        response = model.generate_content(prompt)
        text = response.text
        
        # --- ROBUST CLEANING LOGIC ---
        # 1. Strip out markdown code blocks if AI included them
        text = text.replace("```json", "").replace("```", "").strip()
        
        # 2. Find the first '{' and the last '}' to ignore any AI "chatter"
        start_index = text.find('{')
        end_index = text.rfind('}')
        
        if start_index != -1 and end_index != -1:
            clean_json = text[start_index:end_index+1]
            return json.loads(clean_json)
        else:
            raise ValueError("No valid JSON found in response")
            
    except Exception as e:
        # LOG THE ERROR in your terminal/cloud logs so you can see why it failed
        print(f"AI Formatting Error: {e}")
        
        # FALLBACK: Return a basic plan so the app doesn't show a red crash screen
        # This fallback uses the dietary requirement so it's not totally wrong
        fallback_meal = "Vegan Bowl" if "vegan" in requirements.lower() else "Chicken & Rice"
        return {day: {"Breakfast": "Oats", "Lunch": fallback_meal, "Dinner": fallback_meal} 
                for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}
