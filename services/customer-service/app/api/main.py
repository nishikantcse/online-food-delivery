from fastapi import FastAPI
import psycopg2

app = FastAPI()

def get_connection():
    return psycopg2.connect(
        host="customer-db",   # IMPORTANT (service name)
        database="customer_db",
        user="postgres",
        password="postgres"
    )

@app.get("/v1/customers")
def get_customers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers;")
    rows = cur.fetchall()
    return {"data": rows}