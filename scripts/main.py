from data_ingestion import DataIngestion
from data_cleaning import DataCleaning
from ai_agent import AIAgent

# ✅ Database Configuration
DB_USER = "postgres"  # Replace with your real PostgreSQL username
DB_PASSWORD = ""  # Replace with your PostgreSQL password
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "demodb"

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ✅ Initialize Components
ingestion = DataIngestion(DB_URL)
cleaner = DataCleaning()
ai_agent = AIAgent()

### === 1️⃣ Load and Clean CSV Data === ###
df_csv = ingestion.load_csv("sample_data.csv")
if df_csv is not None:
    print("\n🔹 Cleaning CSV Data...")
    df_csv = cleaner.clean_data(df_csv)
    df_csv = ai_agent.process_data(df_csv)
    print("\n✅ AI-Cleaned CSV Data:\n", df_csv)

### === 2️⃣ Load and Clean Excel Data === ###
df_excel = ingestion.load_excel("sample_data.xlsx")
if df_excel is not None:
    print("\n🔹 Cleaning Excel Data...")
    df_excel = cleaner.clean_data(df_excel)
    df_excel = ai_agent.process_data(df_excel)
    print("\n✅ AI-Cleaned Excel Data:\n", df_excel)

### === 3️⃣ Load and Clean Database Data === ###
df_db = ingestion.load_from_database("SELECT * FROM my_table")  # Change table name
if df_db is not None:
    print("\n🔹 Cleaning Database Data...")
    df_db = cleaner.clean_data(df_db)
    df_db = ai_agent.process_data(df_db)
    print("\n✅ AI-Cleaned Database Data:\n", df_db)

### === 4️⃣ Fetch and Clean API Data === ###
# ✅ Fetch API Data
API_URL = "https://jsonplaceholder.typicode.com/posts"
df_api = ingestion.fetch_from_api(API_URL)

if df_api is not None:
    print("\n🔹 Cleaning API Data...")

    # ✅ Keep only first N rows to avoid token overflow
    df_api = df_api.head(30)  # ✅ Adjust this value based on your dataset size

    # ✅ Reduce long text fields before sending to OpenAI
    if "body" in df_api.columns:
        df_api["body"] = df_api["body"].apply(lambda x: x[:100] + "..." if isinstance(x, str) else x)  # ✅ Limit text length

    df_api = cleaner.clean_data(df_api)
    df_api = ai_agent.process_data(df_api)

    print("\n✅ AI-Cleaned API Data:\n", df_api)
