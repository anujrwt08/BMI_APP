

## 🚀 **Features**

✅ Calculate **BMI** and see your **category** (Underweight, Normal, Overweight, Obese)  
✅ Estimate **BMR** (Basal Metabolic Rate) and **TDEE** (Total Daily Energy Expenditure)  
✅ Get a **calorie target** based on your goal (Maintain, Gain, or Lose Weight)  
✅ View a **sample daily meal plan**  
✅ **Visual BMI gauge chart** using Plotly  
✅ **Downloadable report (TXT)** and **meal plan (CSV)**  
✅ Clean and responsive **Streamlit UI**

---

## 🧮 **How It Works**

1. **Input your details**  
   - Age, Gender, Height, Weight, Activity level, and Goal  
2. **Click "Calculate BMI & Plan"**  
3. The app will:
   - Calculate BMI and show the category  
   - Estimate your calorie needs  
   - Display a gauge chart for your BMI  
   - Suggest a daily meal plan  
4. **Download your personalized report** in TXT or CSV format.

---

## 🧠 Formula References

- **BMI:**  
  \[
  \text{BMI} = \frac{\text{Weight (kg)}}{(\text{Height (m)})^2}
  \]

- **BMR (Mifflin-St Jeor Equation):**  
  - For Men: `BMR = 10W + 6.25H - 5A + 5`  
  - For Women: `BMR = 10W + 6.25H - 5A - 161`

- **TDEE (Total Daily Energy Expenditure):**  
  `TDEE = BMR × Activity Factor`

---

## ⚙️ Installation and Setup

### 1️⃣ Clone this repository
```bash
git clone https://github.com/yourusername/bmi-diet-planner.git
cd bmi-diet-planner
````

### 2️⃣ Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate     # For Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Streamlit app

```bash
streamlit run app.py
```

---

## 📦 Requirements

Create a `requirements.txt` file with the following:

```
streamlit
pandas
plotly
```

---

## 📈 Preview

**Main Page**

* Enter user inputs (age, gender, height, weight, etc.)
* Get BMI results and calorie target

**BMI Gauge Chart**

* Visual indicator for BMI category

**Meal Plan Section**

* Suggests balanced meals according to BMI and goals

**Download Options**

* Save report in `.txt` or `.csv`

---

## 📁 Project Structure

```
bmi_diet_planner/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```

---

## 💡 Future Improvements

* Add user authentication (save previous BMI reports)
* Add custom diet recommendations based on regional foods
* Include macros breakdown (protein, carbs, fats)
* Integration with wearable devices or fitness APIs

---

## 🧑‍💻 Author

**Anuj Rawat**
🎓 — Digital Forensics & Cybersecurity


---

## ⚠️ Disclaimer

This app is for **educational purposes only**.
Calorie and diet recommendations are **approximate** and not a substitute for professional medical or nutritional advice.

---

⭐ **If you like this project, give it a star on GitHub!**
