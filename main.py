import streamlit as st
import numpy as np
import pandas as pd

def calculate(sex, race, treated_BP, age, cl, HDLC, BP, smoker, diabetes):

    # Variable values by sex and race
    if sex == 'Woman':
        if race == "White" or race == "Other":
            coefficients = {
                'age': -29.799,
                'cl': 13.540,
                'HDLC': -13.578,
                'BP': 2.019 if treated_BP else 1.957,
                'smoker': 7.574,
                'diabetes': 0.661
            }
            interaction_coefficients = {
                'lnage_x_lnage': 4.884,
                'lnage_x_lncl': -3.114,
                'lnage_x_lnHDCL': 3.149,
                'lnage_x_lnBP': 0 if treated_BP else 0,
                'lnage_x_smoker': -1.665,
            }
            baseline_survival = 0.9665
            overall_mean_sum = -29.18
        elif race == "Black":
            coefficients = {
                'age': 17.114,
                'cl': 0.940,
                'HDLC': -18.920,
                'BP': 29.291 if treated_BP else 27.820,
                'smoker': 0.691,
                'diabetes': 0.874
            }
            interaction_coefficients = {
                'lnage_x_lnage': 0,
                'lnage_x_lncl': 0,
                'lnage_x_lnHDCL': 4.475,
                'lnage_x_lnBP': -6.432 if treated_BP else -6.087,
                'lnage_x_smoker': 0.691,
            }
            baseline_survival = 0.9533
            overall_mean_sum = 86.61
    elif sex == "Man":
        if race == "White" or race == "Other":
            coefficients = {
                'age': 12.344,
                'cl': 11.853,
                'HDLC': -7.990,
                'BP': 1.797 if treated_BP else 1.764,
                'smoker': 7.837,
                'diabetes': 0.658
            }
            interaction_coefficients = {
                'lnage_x_lnage': 0,
                'lnage_x_lncl': -2.664,
                'lnage_x_lnHDCL': 1.769,
                'lnage_x_lnBP': 0,
                'lnage_x_smoker': -1.795,
            }
            baseline_survival = 0.9144
            overall_mean_sum = 61.18
        elif race == "Black":
            coefficients = {
                'age': 2.469,
                'cl': 0.302,
                'HDLC': -0.307,
                'BP': 1.916 if treated_BP else 1.809,
                'smoker': 0.549,
                'diabetes': 0.645
            }
            interaction_coefficients = {
                'lnage_x_lnage': 0,
                'lnage_x_lncl': 0,
                'lnage_x_lnHDCL': 0,
                'lnage_x_lnBP': 0,
                'lnage_x_smoker': 0,
            }
            baseline_survival = 0.8954
            overall_mean_sum = 19.54
    
    # Algorithm

    # Calculate natural logs of input variables
    ln_age, ln_cl, ln_HDLC, ln_BP = np.log(np.array([age, cl, HDLC, BP]))
    
    # Calculate interaction terms
    lnage_x_lnage = ln_age * ln_age
    lnage_x_lncl = ln_age * ln_cl
    lnage_x_lnHDCL = ln_age * ln_HDLC
    lnage_x_lnBP = ln_age * ln_BP
    lnage_x_smoker = ln_age * smoker

    # Calculate product of interaction term with corresponding coefficient
    interaction_terms = np.array([
        lnage_x_lnage * interaction_coefficients['lnage_x_lnage'],
        lnage_x_lncl * interaction_coefficients['lnage_x_lncl'],
        lnage_x_lnHDCL * interaction_coefficients['lnage_x_lnHDCL'],
        lnage_x_lnBP * interaction_coefficients['lnage_x_lnBP'],
        lnage_x_smoker * interaction_coefficients['lnage_x_smoker']
    ])

    # Calculate product of input variable natural logs and corresponding coefficients
    ln_x_coefficients = np.array([
        ln_age * coefficients['age'],
        ln_cl * coefficients['cl'],
        ln_HDLC * coefficients['HDLC'],
        ln_BP * coefficients['BP'],
        smoker * coefficients['smoker'],
        diabetes * coefficients['diabetes']
    ])

    # Calculate sum of ln_x_coefficients and interaction_x_coefficients
    individual_sum = np.sum(ln_x_coefficients) + np.sum(interaction_terms)

    # Calculate 10 year risk of ASCVD
    risk = 1 - baseline_survival ** np.exp(individual_sum - overall_mean_sum)

    # # Debugging
    # st.subheader("Calculation Results:")
    # st.write("Coefficient Values:")
    # df_coefficients = pd.DataFrame.from_dict(
    #     coefficients, orient='index', columns=['Coefficient'])
    # st.write(df_coefficients)

    # st.write("Interaction Coefficients:")
    # df_interaction = pd.DataFrame.from_dict(
    #     interaction_coefficients, orient='index', columns=['Coefficient'])
    # st.write(df_interaction)

    # st.write("Natural Logarithm of Variables:")
    # df_ln_x = pd.DataFrame(ln_x_coefficients, index=[
    #                        'ln_age', 'ln_cl', 'ln_HDLC', 'ln_BP', 'smoker', 'diabetes'], columns=['Value'])
    # st.write(df_ln_x)

    # st.write("Interaction Terms:")
    # df_interaction_terms = pd.DataFrame(interaction_terms, index=[
    #                                     'lnage_x_lnage', 'lnage_x_lncl', 'lnage_x_lnHDCL', 'lnage_x_lnBP', 'lnage_x_smoker'], columns=['Value'])
    # st.write(df_interaction_terms)

    # st.write("Individual Sum:")
    # st.write(individual_sum)

    # st.write("10-year Risk of ASCVD:")
    # st.write(risk)

    return risk

    

def main():
    st.title("ASCVD Calculator")
    st.markdown(
        "[Evidence](https://www.ahajournals.org/doi/pdf/10.1161/01.cir.0000437741.48606.98)")
    st.write("Enter the required information:")

    sex = st.selectbox("Sex", ["Man", "Woman"])
    race = st.selectbox("Race", ["White", "Black", "Other"])
    treated_BP = st.checkbox("Treatment for hypertension")
    age = st.number_input("Age", value=40, min_value=1)
    cl = st.number_input("Total cholesterol mg/dL", value=200, min_value=1)
    HDLC = st.number_input("HDL cholesterol ml/dL", value=50, min_value=1)
    BP = st.number_input("Systolic blood pressure mm Hg", value=120, min_value=1)
    smoker = int(st.checkbox("Smoker"))
    diabetes = int(st.checkbox("Diabetes"))

    if st.button("Calculate"):
        result = calculate(sex, race, treated_BP, age, cl, HDLC, BP, smoker, diabetes)
        st.write("Your ASCVD risk is:", result)


if __name__ == "__main__":
    main()
