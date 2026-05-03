# services/restaurant-service/app/api/main.py

from fastapi import FastAPI, Request, Response
import psycopg2
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = FastAPI()

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])

@app.middleware('http')
async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status=response.status_code).inc()
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(time.time() - start_time)
    return response

@app.get('/metrics')
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

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