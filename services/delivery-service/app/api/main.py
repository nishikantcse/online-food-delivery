# services/delivery-service/app/api/main.py

from fastapi import FastAPI
import psycopg2

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        host="delivery-db",
        database="delivery_db",
        user="postgres",
        password="postgres"
    )

@app.post("/v1/deliveries/assign")
def assign_driver(delivery: dict):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO deliveries VALUES (%s,%s,%s,'ASSIGNED',NOW(),NULL,NULL)",
        (delivery["delivery_id"], delivery["order_id"], delivery["driver_id"])
    )

    conn.commit()

    return {"message": "Driver assigned"}

@app.patch("/v1/deliveries/{delivery_id}")
def update_status(delivery_id: int, status: dict):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "UPDATE deliveries SET status=%s WHERE delivery_id=%s",
        (status["status"], delivery_id)
    )

    conn.commit()

    return {"message": "Updated"}