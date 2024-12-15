import psycopg2

DATABASE_URL = "postgresql://postgres.gbpiuhyzozcwwcdwrotj:marrZRrR5hc7oC8U@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("Connection successful!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)
