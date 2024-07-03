import psycopg2
from psycopg2 import sql

conn_params = {
    'dbname': 'ruskiy',
    'user': 'magama',
    'password': 'INAAB123',
    'host': 'localhost',  
    'port': '5432'
}

def connectToDB():
    try:
        conn = psycopg2.connect(**conn_params)
        print("Connection successful")
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None
