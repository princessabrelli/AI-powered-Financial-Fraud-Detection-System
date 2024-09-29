import os
import pandas as pd
import streamlit as st
import logging
from model import train_fraud_detection_model, load_model, predict_fraud_probability

logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="AI-Powered Fraud Detection System", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
    }
    h1, h2, h3, h4, h5, h6, p, label, .markdown-text-container {
        color: black;
    }
    input[type="number"] {
        background-color: #f0f0f0;
        color: black;
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 5px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .infographic {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


logo_path = "GuardNet.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=300)
else:
    st.warning("Logo not found.")

st.title("AI-Powered Fraud Detection System")

dataset_path = '/mnt/data/sampled_fraud_dataset.csv'

model_file = 'fraud_detection_model_optimized.pkl'

if os.path.exists(model_file):
    model = load_model(model_file)
    st.success("Model loaded successfully.")
else:
    st.warning("Model not found. Please train the model using the appropriate dataset.")
    
    if st.button("Train Model"):
        try:
            report = train_fraud_detection_model(dataset_path)
            st.text(report)
        except Exception as e:
            st.error(f"An error occurred during training: {e}")
            logging.error(f"Error during model training: {e}")

amount = st.number_input("Amount", min_value=0.0)
oldbalanceOrg = st.number_input("Old Balance of Origin Account", min_value=0.0)
newbalanceOrig = st.number_input("New Balance of Origin Account", min_value=0.0)
oldbalanceDest = st.number_input("Old Balance of Destination Account", min_value=0.0)
newbalanceDest = st.number_input("New Balance of Destination Account", min_value=0.0)

features = [[
    amount, 
    oldbalanceOrg, 
    newbalanceOrig, 
    oldbalanceDest, 
    newbalanceDest
]]

if st.button("Check for Fraud"):
    try:
        fraud_probability = predict_fraud_probability(model, features)
        threshold = 0.50
        if fraud_probability > threshold:
            st.error(f"Fraudulent Transaction Detected! Probability of fraud: {fraud_probability * 100:.2f}%")
        else:
            st.success(f"Transaction is Legitimate. Probability of fraud: {fraud_probability * 100:.2f}%")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
        logging.error(f"Error during fraud detection: {e}")

st.markdown("## Model Performance Infographic", unsafe_allow_html=True)
st.markdown(
    """
    <div class='infographic'>
        <h3>Model Performance Metrics</h3>
        <p><strong>Accuracy:</strong> 99.41%</p>
        <p><strong>Precision for Legitimate Transactions:</strong> 100%</p>
        <p><strong>Recall for Fraudulent Transactions:</strong> 96%</p>
        <p><strong>F1-Score for Fraudulent Transactions:</strong> 96%</p>
        <p><strong>Total Transactions Evaluated:</strong> 20,000</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    ### About This App
    The **AI-Powered Fraud Detection System** helps detect potentially fraudulent transactions in real-time by analyzing transaction data.

    #### Technologies Used:
    **Streamlit**: For building the user interface.\n
    **Scikit-learn**: For training a Random Forest classification model.\n
    **Pandas**: For data manipulation and feature engineering.\n
    **Joblib**: For saving and loading the trained machine learning model.\n
    **Kaggle**: For reliable and massive data sets.\n
    """
)
