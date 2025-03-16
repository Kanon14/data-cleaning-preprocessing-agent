from data_ingestion import DataIngestion
from data_cleaning import DataCleaning
from ai_agent import AIAgent

# Database Configuration
DB_USER = "postgres"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "demodb"

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Initialize components
ingestion = DataIngestion(DB_URL)
cleaner = DataCleaning()
ai_agent = AIAgent()

### === 1. Load and Clean CSV Data === ###
df_csv = ingestion.load_csv("sample_data.csv")
if df_csv is not None:
    print("\n Cleaning CSV Data...")
    df_csv = cleaner.clean_data(df_csv)
    df_csv = ai_agent.process_data(df_csv)
    print("\n CSV Data Cleaned and Processed:\n", df_csv)
    
### === 2. Load and Clean Excel Data === ###
df_excel = ingestion.load_excel("sample_data.xlsx")
if df_excel is not None:
    print("\n Cleaning Excel Data...")
    df_excel = cleaner.clean_data(df_excel)
    df_excel = ai_agent.process_data(df_excel)
    print("\n Excel Data Cleaned and Processed:\n", df_excel)
    
### === 3. Load and Clean Database Data === ###
df_db = ingestion.load_from_database("SELECT * FROM my_table")
if df_db is not None:
    print("\n Cleaning Database Data...")
    df_db = cleaner.clean_data(df_db)
    df_db = ai_agent.process_data(df_db)
    print("\n Database Data Cleaned and Processed:\n", df_db)
    
### === 4. Fetch and Clean API Data === ###
# Fetch API Data
API_URL = "https://jsonplaceholder.typicode.com/posts"
df_api = ingestion.fetch_api(API_URL)

if df_api is not None:
    print("\n Cleaning API Data...")
    
    # Keep only first N rows to avoid token overflow
    df_api = df_api.head(30) 
    
    # Reduce long text fields before sending to OpenAI
    if "body" in df_api.columns:
        df_api["body"] = df_api["body"].apply(lambda x: x[:100] + "..." if isinstance(x, str) else x) # Limit text length
        df_api["body"] = df_api["body"].astype(str)  # Convert to string type to avoid OpenAI error
    
    df_api = cleaner.clean_data(df_api)
    df_api = ai_agent.process_data(df_api)
    
    print("\n API Data Cleaned and Processed:\n", df_api)