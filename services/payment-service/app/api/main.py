# services/payment-service/app/api/main.py

from fastapi import FastAPI, Header, HTTPException
import psycopg2

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        host="payment-db",
        database="payment_db",
        user="postgres",
        password="postgres"
    )

@app.post("/v1/payments/charge")
def charge(payment: dict, idempotency_key: str = Header(None)):

    conn = get_conn()
    cur = conn.cursor()

    # Check idempotency
    cur.execute("SELECT * FROM idempotency_keys WHERE idempotency_key=%s", (idempotency_key,))
    if cur.fetchone():
        return {"message": "Duplicate request"}

    # Insert payment
    cur.execute(
        "INSERT INTO payments VALUES (%s,%s,%s,%s,'SUCCESS','ref123',NOW())",
        (payment["payment_id"], payment["order_id"], payment["amount"], payment["method"])
    )

    cur.execute(
        "INSERT INTO idempotency_keys (idempotency_key,response) VALUES (%s,%s)",
        (idempotency_key, "success")
    )

    conn.commit()

    return {"status": "SUCCESS"}