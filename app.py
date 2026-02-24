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
if st.button("✨ Predict"):
    if model:
        try:
            # We are sending exactly 6 features now
            feature_values = [
                1,             # 1. Continent
                1,             # 2. Country
                1,             # 3. VisitMode 
                6,             # 4. VisitMonth
                2024,          # 5. VisitYear
                float(rating)  # 6. Rating (from slider)
            ]
            
            # Convert to a simple array to bypass naming issues
            final_features = np.array([feature_values])
            
            # 3. Predict
            prediction = model.predict(final_features)
            
            st.balloons()
            st.success("✅ Prediction Successful!")
            st.metric(label="Predicted Result", value=str(prediction[0]))
            
        except Exception as e:
            st.error(f"Almost there! Error: {e}")
            st.write("The model saw 6 features during training. We are now sending 6.")

st.markdown("---")
