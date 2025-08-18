import streamlit as st

def macro_calculator(total_body_weight_lbs, body_fat_percent, total_calories=None):
    # Calculate LBM
    lbm_lbs = total_body_weight_lbs * (1 - body_fat_percent/100)
    lbm_kg = lbm_lbs / 2.205

    # Protein: 2.5 g/kg LBM
    protein_g = round(lbm_kg * 2.5)

    # Carbs: 3.75 g/kg LBM
    carbs_g = round(lbm_kg * 3.75)

    # Fat: minimum 0.3 g/kg LBM or fill calories if target provided
    if total_calories:
        kcal_from_protein = protein_g * 4
        kcal_from_carbs = carbs_g * 4
        remaining_kcal = max(total_calories - (kcal_from_protein + kcal_from_carbs), 0)
        fats_g = round(remaining_kcal / 9)
        fats_min = round(lbm_kg * 0.3)
        fats_g = max(fats_g, fats_min)
    else:
        fats_g = round(lbm_kg * 0.3)

    # Calculate total kcal
    kcal_total = protein_g * 4 + carbs_g * 4 + fats_g * 9

    return lbm_lbs, protein_g, carbs_g, fats_g, kcal_total


# Streamlit app
st.title("Macronutrient Calculator (LBM-based)")

st.write("This tool calculates your macros using lean body mass with your custom parameters:")
st.write("- Protein: 2.5 g/kg LBM")
st.write("- Carbs: 3.75 g/kg LBM")
st.write("- Fat: minimum 0.3 g/kg LBM or more if calorie target requires")

# User inputs
weight = st.number_input("Enter your total body weight (lbs):", min_value=50.0, max_value=600.0, step=1.0)
body_fat = st.number_input("Enter your body fat percentage (%):", min_value=1.0, max_value=70.0, step=0.5)
calorie_target = st.number_input("Optional: Enter your calorie target (kcal):", min_value=0, step=50)

if st.button("Calculate Macros"):
    total_calories = calorie_target if calorie_target > 0 else None
    lbm_lbs, protein, carbs, fats, kcal_total = macro_calculator(weight, body_fat, total_calories)

    st.subheader("Your Macro Breakdown")
    st.write(f"**Lean Body Mass:** {lbm_lbs:.1f} lbs")
    st.write(f"**Protein:** {protein} g")
    st.write(f"**Carbs:** {carbs} g")
    st.write(f"**Fat:** {fats} g")
    st.write(f"**Calories:** {kcal_total} kcal")
