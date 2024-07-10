# upload.py
import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

def load_model(): 
    model_path = "GARFB.pkl"
    st.write(f"Attempting to load model from: {model_path}")  # Debug statement

    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        st.error(f"Model file not found at: {model_path}")
        return None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def upload_and_predict():
    uploaded_file = st.file_uploader("Choose your CSV file", type="csv")
    if uploaded_file is not None: 
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data:")
        st.write(df)

        if 'Class' in df.columns:
            X = df.drop("Class", axis=1)
        else:
            st.error("The uploaded file does not contain a 'Class' column.")
            return None

        model = load_model()

        if model:
            predictions = model.predict(X)
            df['Prediction'] = predictions
            df['Prediction'] = df['Prediction'].map({0: 'Not Fraudulent', 1: 'Fraudulent'})

            st.write("Predictions:")
            st.write(df)

            st.download_button(
                label="Download Predictions as CSV", 
                data=df.to_csv(index=False),
                file_name='predictions.csv',
                mime='text/csv'
            )

            return df
    return None
