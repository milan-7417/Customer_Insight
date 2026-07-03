import os
import pandas as pd
import streamlit as st
from utils.data_generator import generate_customer_dataset

@st.cache_data
def load_customer_data():
    """Loads the e-commerce customer behavior dataset.
    Generates it first if the file does not exist.
    """
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(workspace_root, "data", "customer_data.csv")
    
    # Generate dataset if it's missing
    if not os.path.exists(data_path):
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        generate_customer_dataset(data_path)
        
    df = pd.read_csv(data_path)
    
    # Minor cleanups or conversions
    # E.g., make sure Customer_ID is unique, convert datatypes if required
    # Convert Churn_Status to boolean if not already
    df['Churn_Status'] = df['Churn_Status'].astype(bool)
    
    return df
