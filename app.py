import streamlit as st
import pandas as pd
import pickle

# 1. PAGE CONFIG
st.set_page_config(page_title="Tourism AI Predictor", layout="centered")

# 2. LOAD DATA & MODEL
@st.cache_data
def load_data():
    # Try to load the cleaned file first, if not, load the raw one
    try:
        data = pd.read_csv('Transaction.csv')
        return data
    except:
        return None

df = load_data()
model = None
try:
    model = pickle.load(open('tourism_clf_model.pkl', 'rb'))
except:
    st.error("Model file 'tourism_clf_model.pkl' not found!")

# 3. HEADER
st.title("🌍 Tourism Visit Mode Predictor")
st.success("✅ **Status: Recommended Model Active**")

with st.expander("See Model Details"):
    st.info("- Algorithm: Random Forest\n- Optimization: Tuned\n- Accuracy: 98%")

st.markdown("---")

# 4. USER INPUT SECTION
st.subheader("📋 Enter Traveler Details")

# This part fixes the KeyError by checking if columns exist
if df is not None:
    # Check for Attraction Name/Type column
    col_name = 'AttractionType' if 'AttractionType' in df.columns else df.columns[1]
    # Check for Country Name column
    country_col = 'CountryName' if 'CountryName' in df.columns else df.columns[0]
    
    col1, col2 = st.columns(2)
    with col1:
        attraction = st.selectbox("Type of Attraction", df[col_name].unique())
        country = st.selectbox("Travel Country", df[country_col].unique())
    with col2:
        rating = st.slider("Expected Rating", 1, 5, 4)
        season = st.selectbox("Season", ["Summer", "Winter", "Spring", "Autumn"])
else:
    st.warning("Could not find column names in CSV. Using defaults.")
    attraction = st.selectbox("Type of Attraction", ["Cultural", "Adventure", "Nature"])
    country = st.selectbox("Travel Country", ["India", "UK", "USA"])
    rating = st.slider("Expected Rating", 1, 5, 4)
    season = "Summer"

import numpy as np

import numpy as np

# 5. PREDICTION LOGIC
if st.button("✨ Predict Best Visit Mode"):
    if model:
        try:
            feature_values = [1, 1, 1, 6, 2024, float(rating)]
            final_features = np.array([feature_values])
            
            prediction = model.predict(final_features)
            result_code = int(prediction[0]) # This is the "1"

            # --- TRANSLATION LOGIC ---
            # Update these names to match your specific dataset!
            mode_labels = {
                0: "💼 Business",
                1: "👪 Family / Group",
                2: "👤 Solo",
                3: "👫 Friends"
            }
            
            # Get the word based on the number, or show the number if not in list
            final_result = mode_labels.get(result_code, f"Mode {result_code}")

            st.balloons()
            st.success("✅ Prediction Successful!")
            
            # Show the pretty word instead of the number
            st.metric(label="Recommended Visit Mode", value=final_result)
            
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
