# services/order-service/app/api/main.py

from fastapi import FastAPI, HTTPException
import psycopg2
import requests

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        host="order-db",
        database="order_db",
        user="postgres",
        password="postgres"
    )

@app.post("/v1/orders")
def create_order(order: dict):

    # 1. Validate restaurant
    r = requests.get(f"http://restaurant-service:8000/v1/restaurants")
    restaurants = r.json()["data"]

    if not any(res[0] == order["restaurant_id"] for res in restaurants):
        raise HTTPException(400, "Restaurant closed or not found")

    # 2. Calculate total
    total = 0
    for item in order["items"]:
        total += item["price"] * item["quantity"]

    total = total + (0.05 * total) + 30  # tax + delivery

    # 3. Save order
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO orders VALUES (%s,%s,%s,%s,'CREATED',%s,'PENDING',NOW())",
        (order["order_id"], order["customer_id"], order["restaurant_id"], order["address_id"], total)
    )

    for item in order["items"]:
        cur.execute(
            "INSERT INTO order_items VALUES (%s,%s,%s,%s,%s)",
            (item["order_item_id"], order["order_id"], item["item_id"], item["quantity"], item["price"])
        )

    conn.commit()

    return {"message": "Order created", "total": total}

@app.get("/v1/orders/{order_id}")
def get_order(order_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE order_id=%s", (order_id,))
    return {"data": cur.fetchone()}