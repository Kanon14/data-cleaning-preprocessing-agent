import os
import pandas as pd
import requests
from sqlalchemy import create_engine

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")

class DataIngestion:
    def __init__(self, db_url=None):
        """Initialize data ingestion with an optimal database connection."""
        self.engine = create_engine(db_url) if db_url else None
        
    def load_csv(self, file_name):
        """Loads a csv file into a DataFrame."""
        file_path = os.path.join(DATA_DIR, file_name)
        try:
            df = pd.read_csv(file_path)
            print(f"✅ Successfully loaded {file_name} into a DataFrame.")
            return df
        except Exception as e:
            print(f"❌ Error loading {file_name} into a DataFrame. Error: {e}")
            return None
        
    def load_excel(self, file_name, sheet_name=0):
        """Loads an Excel file into a DataFrame."""
        file_path = os.path.join(DATA_DIR, file_name)
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"✅ Successfully loaded {file_name} into a DataFrame.")
            return df
        except Exception as e:
            print(f"❌ Error loading {file_name} into a DataFrame. Error: {e}")
            return None
        
    def connect_database(self, db_url):
        """Establish a database connection."""
        try:
            self.engine = create_engine(db_url)
            print("✅ Successfully connected to the database.")
        except Exception as e:
            print(f"❌ Error connecting to the database. Error: {e}")
            
    def load_from_database(self, query):
        """Fetches data from a database using SQL."""
        if not self.engine:
            print("❌ No database connection established. Call connect_database() first.")
            return None
        try:
            df = pd.read_sql(query, self.engine)
            print("✅ Data Loaded from database sucessfully.")
            return None
        except Exception as e:
            print(f"❌ Error loading data from the database. Error: {e}")
            
    def fetch_api(self, api_url, params=None):
        """Fetches data from an API and returns it as a DataFrame."""
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                print(f"✅ Data fetched from API successfully.")
                return df
            else:
                print(f"❌ Error fetching data from API. Status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching data from API. Error: {e}")
            return None
