# services/customer-service/app/api/main.py

from fastapi import FastAPI, HTTPException
import psycopg2

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        host="customer-db",
        database="customer_db",
        user="postgres",
        password="postgres"
    )

@app.post("/v1/customers")
def create_customer(customer: dict):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO customers VALUES (%s,%s,%s,%s,NOW())",
        (customer["customer_id"], customer["name"], customer["email"], customer["phone"])
    )
    conn.commit()
    return {"message": "Customer created"}

@app.get("/v1/customers")
def get_customers():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    return {"data": cur.fetchall()}

@app.get("/v1/customers/{customer_id}/addresses")
def get_addresses(customer_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM addresses WHERE customer_id=%s", (customer_id,))
    return {"data": cur.fetchall()}