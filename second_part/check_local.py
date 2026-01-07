import sys
import os

print("Checking environment...")
print(f"Python: {sys.version}")

try:
    import psycopg2
    print("SUCCESS: psycopg2 is installed.")
except ImportError:
    print("ERROR: psycopg2 is NOT installed. Run 'pip install psycopg2-binary'")
    sys.exit(1)

try:
    import login
    print("SUCCESS: login.py found.")
    print(f"Connecting to {login.host}...")
    conn = psycopg2.connect(login.credentials)
    print("SUCCESS: Connected to database!")
    conn.close()
except Exception as e:
    print(f"ERROR: Database connection failed. {e}")
    print("Make sure you are on VPN and login.py has correct credentials.")
