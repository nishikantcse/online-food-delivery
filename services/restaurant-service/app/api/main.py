# services/restaurant-service/app/api/main.py

from fastapi import FastAPI
import psycopg2

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        host="restaurant-db",
        database="restaurant_db",
        user="postgres",
        password="postgres"
    )

@app.get("/v1/restaurants")
def get_restaurants():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM restaurants WHERE is_open=true")
    return {"data": cur.fetchall()}

@app.get("/v1/restaurants/{restaurant_id}/menu")
def get_menu(restaurant_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM menu_items WHERE restaurant_id=%s AND is_available=true",
        (restaurant_id,)
    )
    return {"data": cur.fetchall()}