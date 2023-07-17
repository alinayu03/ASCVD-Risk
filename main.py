import streamlit as st
import numpy as np

def calculate(sex, race, treated_BP, age, cl, HDLC, BP, smoker, diabetes):
    if sex == 'woman':
        if race == "white":
            coefficients = {
                'age': -29.799,
                'cl': 13.540,
                'HDLC': -13.578,
                'BP': 2.019 if treated_BP else 1.957,
                'smoker': 7.574,
                'diabetes': 0.661
            }

        lns = np.log(np.array([age, cl, HDLC, BP, smoker, diabetes]))
        result = lns * np.array([coefficients[key] for key in coefficients])
        return result



# inputs

age = st.number_input('Age', )