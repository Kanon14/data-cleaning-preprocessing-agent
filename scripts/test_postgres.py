import psycopg2

# Setting DB credentials
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "demodb"
DB_USER = "postgres"
DB_PASSWORD = ""

# Connecting to the database
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    print("Connected to the PostgreSQL database successfully!")

    # Execute a test query
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cursor.fetchall()

    if tables:
        print("Tables in the database:")
        for table in tables:
            print(f"- {table[0]}")
    else:
        print("No tables found in the database.")

except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL: {e}")

finally:
    # Closing the cursor and connection
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()
        print("Database connection closed.")
