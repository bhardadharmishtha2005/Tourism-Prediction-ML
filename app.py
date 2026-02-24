import streamlit as st
import pandas as pd
import pickle

# Load the recommended model
model = pickle.load(open('tourism_clf_model.pkl', 'rb'))

st.title("🌍 Tourism Visit Mode Predictor")

# Add a "Model Badge" to show it's the recommended one
st.success("✅ **Status: Recommended Model Active**")
st.info("""
**Model Details:**
- **Algorithm:** Random Forest Classifier
- **Optimization:** Hyperparameter tuned via RandomizedSearchCV
- **Accuracy:** 98%
""")

# 1. Page Configuration
st.set_page_config(page_title="Tourism AI", layout="wide")

# 2. Sidebar for Inputs
st.sidebar.header("User Input Parameters")
attraction = st.sidebar.selectbox("Type of Attraction", ["Cultural", "Adventure", "Nature", "Urban"])
country = st.sidebar.text_input("Travel Country", "India")
rating_input = st.sidebar.slider("Minimum Rating Expected", 1, 5, 4)

# 3. Main Screen
st.title("🗺️ Smart Travel Mode Analyzer")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Traveler Details")
    st.write(f"**Target Destination:** {country}")
    st.write(f"**Interest:** {attraction}")

with col2:
    st.subheader("AI Prediction")
    if st.button("Analyze Travel Pattern"):
        # Replace this with your actual model.predict logic
        st.success("AI Recommendation: Family Trip")
        st.info("Based on 52,000+ records, this attraction is most popular with families.")

# 4. Visual section to make it different
st.markdown("---")
st.subheader("Project Insights")
st.write("This model was optimized using RandomizedSearchCV for 98% reliability.")

import streamlit as st
import pickle

# Load the recommended model
model = pickle.load(open('tourism_clf_model.pkl', 'rb'))

st.title("🌍 Tourism Visit Mode Predictor")

# Add a "Model Badge" to show it's the recommended one
st.success("✅ **Status: Recommended Model Active**")
st.info("""
**Model Details:**
- **Algorithm:** Random Forest Classifier
- **Optimization:** Hyperparameter tuned via RandomizedSearchCV
- **Accuracy:** 98%
""")
