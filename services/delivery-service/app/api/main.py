# services/delivery-service/app/api/main.py

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