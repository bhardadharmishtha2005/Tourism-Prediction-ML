import streamlit as st
import pandas as pd
import pickle

# Load the model
model = pickle.load(open('tourism_clf_model.pkl', 'rb'))

st.title("🌍 Tourism Visit Mode Predictor")
st.write("Enter details to predict if the traveler is Solo, Family, or a Couple.")

# Simple inputs based on your data
attraction = st.selectbox("Select Attraction Type", ["Cultural", "Adventure", "Nature", "Urban"])
country = st.text_input("Enter Country Name", "India")

if st.button("Predict"):
    # This is a placeholder for the actual prediction logic
    st.success("The predicted Visit Mode is: Family")
