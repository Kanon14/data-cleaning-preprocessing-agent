import streamlit as st
import requests
import pandas as pd
import json
from io import StringIO

# FastAPI Backend URL
FASTAPI_URL = "https://127.0.0.1:8000"

# Streamlit UI Configuration
st.set_page_config(page_title="AI-Powered Data Cleaning", layout="wide")

# Sidebar - Data Source Selection
st.sidebar.header("📊 Data Source Selection")
data_source = st.sidebar.radio(
    "Select Data Source:",
    ["CSV/Excel", "Database Query", "API Data"],
    index=0
)

# Main Title
st.markdown("""
            # 🧹 **AI-Powered Data Cleaning**
            *Clean your data effortlessly using the AI-Powered Data Cleaning*
            """)

# Handling CSV/Excel Upload
if data_source == "CSV/Excel":
    st.subheader("📂 Upload File for Cleaning")
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension == "xlsx":
            df = pd.read_excel(uploaded_file)
        
        st.write("### 🔍 Raw Data Preview:")
        st.dataframe(df)
        
        if st.button("✨ Clean Data"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(f"{FASTAPI_URL}/clean-data", files=files)
            
            if response.status_code == 200:
                st.subheader("🔍 Raw API Response (Debugging)")
                st.json(response.json()) # Debugging: Check actual response format
                
                # Parse cleaned data properly
                try:
                    cleaned_data_raw = response.json()["cleaned_data"]
                    if isinstance(cleaned_data_raw, str):
                        cleaned_data = pd.DataFrame(json.loads(cleaned_data_raw)) # Convert string JSON to dict
                    else:
                        cleaned_data = pd.DataFrame(cleaned_data_raw) # Assume it's a list of dicts
                        
                    st.subheader("✅ Cleaned Data:")
                    st.dataframe(cleaned_data)
                except Exception as e:
                    st.error(f"❌ Error parsing cleaned data: {e}")
            else:
                st.error(f"❌ Error cleaning data: {response.status_code} - {response.text}")
                
# Handling Database Query