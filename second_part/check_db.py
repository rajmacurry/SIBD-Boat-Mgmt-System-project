import psycopg2
import login
from psycopg2 import sql

def check_db():
    try:
        conn = psycopg2.connect(login.credentials)
        cur = conn.cursor()
        
        print("Connected.")
        
        # 1. Check schemas
        cur.execute("SELECT schema_name FROM information_schema.schemata;")
        schemas = [row[0] for row in cur.fetchall()]
        print(f"Available Schemas: {schemas}")
        
        if 'project_2' not in schemas:
            print("Schema 'project_2' does not exist.")
            # Verify if generic tables exist in public
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
            tables = [row[0] for row in cur.fetchall()]
            print(f"Tables in public: {tables}")
        else:
            print("Schema 'project_2' exists.")
            cur.execute("SET search_path TO project_2;")
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='project_2';")
            tables = [row[0] for row in cur.fetchall()]
            print(f"Tables in project_2: {tables}")
            
            if 'sailor' in tables:
                print("Table 'sailor' found in project_2.")
            else:
                print("Table 'sailor' NOT found in project_2.")

        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    check_db()
