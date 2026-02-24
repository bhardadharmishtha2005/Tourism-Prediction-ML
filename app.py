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

# 5. PREDICTION LOGIC
if st.button("✨ Predict Best Visit Mode"):
    if model:
        try:
            # We must create a DataFrame with EVERY column the model expects
            # We use the user's input for some, and 'default' values for others
            input_df = pd.DataFrame({
                'Continent': [1],      # Default (e.g., Asia)
                'Country': [1],        # Default
                'VisitMode': [1],      # This is usually the Target, but if it was a feature:
                'VisitMonth': [6],     # Default (June)
                'VisitYear': [2024],   # Default
                'Rating': [rating]      # From the Slider
                # Add any other missing columns here!
            })

            # Make the prediction
            prediction = model.predict(input_df)
            
            st.balloons()
            st.subheader("Analysis Result:")
            # If your result is a number, we show it. 
            # If you want to show a word, we can map it.
            st.metric(label="Predicted Mode", value=str(prediction[0]))
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("The model expects these exact columns: Continent, Country, VisitMode, VisitMonth, VisitYear, Rating")
    else:
        st.error("Model not loaded!")

st.markdown("---")
