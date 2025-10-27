import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go

# ----------------------
# BMI + Diet Planner App
# ----------------------

st.set_page_config(page_title="BMI Calculator & Diet Planner", layout="centered")
st.title("🩺 BMI Calculator + Diet Planner")
st.write("Calculate your BMI, see your category, get a daily calorie target and a simple sample diet plan.")

# --- User inputs ---
with st.form(key='bmi_form'):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age (years)", min_value=5, max_value=120, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"]) 
        height_cm = st.slider("Height (cm)", min_value=100, max_value=220, value=170)
    with col2:
        weight_kg = st.slider("Weight (kg)", min_value=30, max_value=200, value=70)
        activity = st.selectbox("Activity level", [
            "Sedentary (little or no exercise)",
            "Lightly active (light exercise/sports 1-3 days/week)",
            "Moderately active (moderate exercise/sports 3-5 days/week)",
            "Very active (hard exercise/sports 6-7 days/week)",
            "Extra active (very hard exercise or physical job)"
        ])
        goal = st.selectbox("Goal", ["Maintain weight", "Mild weight loss", "Weight loss", "Mild weight gain", "Weight gain"]) 

    submit = st.form_submit_button("Calculate BMI & Plan")

# --- Helper functions ---

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100.0
    return weight / (height_m ** 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def activity_factor(level):
    mapping = {
        "Sedentary (little or no exercise)": 1.2,
        "Lightly active (light exercise/sports 1-3 days/week)": 1.375,
        "Moderately active (moderate exercise/sports 3-5 days/week)": 1.55,
        "Very active (hard exercise/sports 6-7 days/week)": 1.725,
        "Extra active (very hard exercise or physical job)": 1.9
    }
    return mapping.get(level, 1.2)


def bmr_mifflin(weight, height_cm, age, gender):
    # Mifflin-St Jeor Equation
    if gender == "Male":
        return 10 * weight + 6.25 * height_cm - 5 * age + 5
    elif gender == "Female":
        return 10 * weight + 6.25 * height_cm - 5 * age - 161
    else:
        # for 'Other' use average of male & female equations
        male = 10 * weight + 6.25 * height_cm - 5 * age + 5
        female = 10 * weight + 6.25 * height_cm - 5 * age - 161
        return (male + female) / 2


def adjust_calorie_for_goal(tdee, goal):
    # mild loss = -250, loss = -500, mild gain = +250, gain = +500
    mapping = {
        "Maintain weight": 0,
        "Mild weight loss": -250,
        "Weight loss": -500,
        "Mild weight gain": 250,
        "Weight gain": 500
    }
    return int(tdee + mapping.get(goal, 0))


def sample_meal_plan(cal_target, category):
    # Simple balanced sample plans — approximate calories
    # Split: Breakfast 25%, Lunch 35%, Snack 10%, Dinner 30%
    b = int(cal_target * 0.25)
    l = int(cal_target * 0.35)
    s = int(cal_target * 0.10)
    d = int(cal_target * 0.30)

    if category == "Underweight":
        notes = "Focus on calorie-dense nutritious foods: nuts, dairy, healthy oils, and protein."
        breakfast = f"Oats with whole milk, banana, and peanut butter (~{b+150} kcal)"
        lunch = f"Rice/roti + dal + paneer/chicken + veggies (~{l+200} kcal)"
        snack = f"Nuts & dried fruit or smoothie (~{s+150} kcal)"
        dinner = f"Rice/roti + lentils + salad + yogurt (~{d+150} kcal)"
    elif category == "Normal weight":
        notes = "Maintain balanced macros and regular activity."
        breakfast = f"Vegetable omelette/tofu scramble + wholegrain toast (~{b} kcal)"
        lunch = f"Grilled chicken/fish or paneer + salad + brown rice (~{l} kcal)"
        snack = f"Fruit or yogurt (~{s} kcal)"
        dinner = f"Light curry + roti + salad (~{d} kcal)"
    elif category == "Overweight":
        notes = "Reduce refined carbs & added sugars; prioritize protein and fiber."
        breakfast = f"Greek yogurt + berries + seeds (~{b-100} kcal)"
        lunch = f"Grilled protein + large salad + quinoa (~{l-100} kcal)"
        snack = f"Raw veggies or an apple (~{s-50} kcal)"
        dinner = f"Steamed fish/beans + veggies (~{d-50} kcal)"
    else:  # Obese
        notes = "Aim for modest calorie deficit, high fiber, lean proteins. Consult a professional for personalised plan."
        breakfast = f"Oatmeal with berries (~{int(b-150)} kcal)"
        lunch = f"Large salad with lean protein (~{int(l-150)} kcal)"
        snack = f"Veg sticks or a small fruit (~{int(s-50)} kcal)"
        dinner = f"Light vegetable soup + lean protein (~{int(d-100)} kcal)"

    return {
        "notes": notes,
        "breakfast": breakfast,
        "lunch": lunch,
        "snack": snack,
        "dinner": dinner
    }

# --- Main logic ---
if submit:
    bmi = calculate_bmi(weight_kg, height_cm)
    category = bmi_category(bmi)
    bmr = bmr_mifflin(weight_kg, height_cm, age, gender)
    tdee = int(bmr * activity_factor(activity))
    cal_target = adjust_calorie_for_goal(tdee, goal)

    st.markdown("### 📊 Results")
    st.write(f"**BMI:** {bmi:.2f} — **Category:** {category}")
    st.write(f"**Estimated BMR:** {int(bmr)} kcal/day — **Estimated TDEE:** {tdee} kcal/day")
    st.info(f"Recommended daily calorie target based on your goal: **{cal_target} kcal/day**")

    # BMI gauge chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = bmi,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "BMI"},
        gauge = {
            'axis': {'range': [10, 40]},
            'steps': [
                {'range': [10, 18.5], 'color': "lightblue"},
                {'range': [18.5, 25], 'color': "lightgreen"},
                {'range': [25, 30], 'color': "yellow"},
                {'range': [30, 40], 'color': "lightcoral"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': bmi
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Meal plan
    plan = sample_meal_plan(cal_target, category)
    st.markdown("### 🍽️ Sample Daily Meal Plan")
    st.write(f"**Notes:** {plan['notes']}")
    st.write(f"**Breakfast:** {plan['breakfast']}")
    st.write(f"**Lunch:** {plan['lunch']}")
    st.write(f"**Snack:** {plan['snack']}")
    st.write(f"**Dinner:** {plan['dinner']}")

    st.markdown("---")

    # Exportable report
    report = "BMI Report\n"
    report += f"Age: {age}\nGender: {gender}\nHeight (cm): {height_cm}\nWeight (kg): {weight_kg}\n\n"
    report += f"BMI: {bmi:.2f} ({category})\nBMR: {int(bmr)} kcal/day\nTDEE: {tdee} kcal/day\nCalorie target: {cal_target} kcal/day\n\n"
    report += "Sample Meal Plan:\n"
    report += f"Breakfast: {plan['breakfast']}\n"
    report += f"Lunch: {plan['lunch']}\n"
    report += f"Snack: {plan['snack']}\n"
    report += f"Dinner: {plan['dinner']}\n"

    st.download_button("📥 Download BMI report (TXT)", report, file_name="bmi_report.txt")

    # CSV of meal plan
    df_plan = pd.DataFrame({"meal": ["Breakfast","Lunch","Snack","Dinner"],
                            "suggestion": [plan['breakfast'], plan['lunch'], plan['snack'], plan['dinner']]})
    csv_buf = io.StringIO()
    df_plan.to_csv(csv_buf, index=False)
    st.download_button("📥 Download meal plan (CSV)", csv_buf.getvalue(), file_name="meal_plan.csv", mime="text/csv")

    st.success("Done — use this plan as a starting point. For personalised medical or dietary advice consult a professional.")

st.caption("Built for educational purposes. Calorie estimates are approximate.")


