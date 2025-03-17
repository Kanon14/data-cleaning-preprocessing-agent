import sys
import os
import pandas as pd
import io
import aiohttp
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from sqlalchemy import create_engine
from pydantic import BaseModel
import requests

# Ensure the scripts folder is in Python's path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from scripts.ai_agent import AIAgent # Import AI agent
from scripts.data_cleaning import DataCleaning # Import Rule-Based Data Cleaning

app = FastAPI()

# Initializing AI agent and rule-based data cleaner
ai_agent = AIAgent()
cleaner = DataCleaning()

# ---------------- CSV / Excel Cleaning Endpoint ---------------- #

@app.post("/clean-data")
async def clean_data(file: UploadFile = File(...)):
    """Receives file from UI, cleans it using rule-based & AI methods, and returns cleaned JSON."""
    try:
        contents = await file.read()
        file_extension = file.filename.split('.')[-1]
        
        # Load file into Pandas DataFrame
        if file_extension == "csv":
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')), on_bad_lines="skip")
        elif file_extension in ["xlsx", "xls"]:
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Invalid file format. Only CSV and Excel files are supported.")
        
        # Step 1: Rule-Based Cleaning
        df_cleaned = cleaner.clean_data(df)
        
        # Step 2: AI-Powered Cleaning
        df_ai_cleaned = ai_agent.process_data(df_cleaned)
        
        # Ensure AI output is a DataFrame
        if isinstance(df_ai_cleaned, str):
            from io import StringIO
            df_ai_cleaned = pd.read_csv(StringIO(df_ai_cleaned))
            
        return {"cleaned_data": df_ai_cleaned.to_dict(orient="records")}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
# ---------------- Database Query Cleaning Endpoint ---------------- #

class DBQuery(BaseModel):
    db_url: str
    query: str
    
@app.post("/clean-db")
async def clean_db(query: DBQuery):
    """Fetches data from a database, cleans it using AI, and return cleaned JSON."""
    try:
        engine = create_engine(query.db_url)
        df = pd.read_sql(query.query, engine)
        
        # Step 1: Rule-Based Cleaning
        df_cleaned = cleaner.clean_data(df)
        
        # Step 2: AI-Powered Cleaning
        df_ai_cleaned = ai_agent.process_data(df_cleaned)
        
        # Ensure AI output is a DataFrame
        if isinstance(df_ai_cleaned, str):
            from io import StringIO
            df_ai_cleaned = pd.read_csv(StringIO(df_ai_cleaned))
            
        return {"cleaned_data": df_ai_cleaned.to_dict(orient="records")}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing database query: {str(e)}")
    
# ---------------- API Data Cleaning Endpoint ---------------- #

class APIRequest(BaseModel):
    api_url: str

@app.post("/clean-api")
async def clean_api(api_request: APIRequest):
    """Fetches data from an API, cleans it using AI, and returns cleaned JSON."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_request.api_url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status, detail="API request failed.")
                
                data = await response.json()
                df = pd.DataFrame(data)
                
                # Step 1: Rule-Based Cleaning
                df_cleaned = cleaner.clean_data(df)
                
                # Step 2: AI-Powered Cleaning
                df_ai_cleaned = ai_agent.process_data(df_cleaned)
                
                # Ensure AI output is a DataFrame
                if isinstance(df_ai_cleaned, str):
                    from io import StringIO
                    df_ai_cleaned = pd.read_csv(StringIO(df_ai_cleaned))
                
                return {"cleaned_data": df_ai_cleaned.to_dict(orient="records")}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing API request: {str(e)}")
    
# ---------------- Run Server ---------------- #

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)