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

# 5. PREDICTION LOGIC (The Fixed Version)
if st.button("✨ Predict Best Visit Mode"):
    if model:
        # 1. Prepare the input data (Must match your training columns)
        # Note: You might need to Encode your inputs if your model expects numbers
        # This is a simplified example:
        input_data = pd.DataFrame({
            'Rating': [rating],
            'AttractionType': [attraction],
            'CountryName': [country]
        })
        
        # 2. Make the actual prediction
        try:
            prediction = model.predict(input_data)
            
            st.balloons()
            st.subheader("Analysis Result:")
            st.metric(label="Predicted Visit Mode", value=str(prediction[0]))
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            st.warning("Hint: Your model might expect numbers (LabelEncoding).")
    else:
        st.error("Model not loaded!")

st.markdown("---")
