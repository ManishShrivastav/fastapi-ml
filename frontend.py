import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.title("Insurance Premium Category Prediction")

st.markdown("Enter the details below to predict the insurance premium category:")

# Input fields
age = st.number_input("Age", min_value=1, max_value=120, value=30)
weight = st.number_input("Weight (kg)", min_value=0.1, value=70.0)
height = st.number_input("Height (m)", min_value=0.1, max_value=2.5, value=1.75)
income_lpa = st.number_input("Annual Income (lpa)", min_value=0.1, value=5.0)
smoker = st.checkbox("Are you a smoker?", options=["True", "False"])
city = st.text_input("City of residence", value="Mumbai")
occupation = st.selectbox("Occupation", options=['retired','freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'])