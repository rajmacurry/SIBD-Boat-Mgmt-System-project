import psycopg2
from psycopg2 import Error
import login

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """Connect to the PostgreSQL database server"""
        try:
            # Using the credentials string from login.py
            self.connection = psycopg2.connect(login.credentials)
            # Create a cursor to perform database operations
            self.cursor = self.connection.cursor()
            print(f"Connected to database '{login.db_name}' successfully.")
            return True
        except (Exception, Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}")
            return False

    def close(self):
        """Close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("PostgreSQL connection is closed")

    def execute_query(self, query, params=None):
        """Execute a read query (SELECT)"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except (Exception, Error) as error:
            print(f"Error executing query: {error}")
            return None
