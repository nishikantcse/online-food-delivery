# services/customer-service/app/api/main.py

from fastapi import FastAPI, HTTPException, Request, Response
import psycopg2
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = FastAPI()

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])

def get_conn():
    return psycopg2.connect(
        host="customer-db",
        database="customer_db",
        user="postgres",
        password="postgres"
    )

@app.middleware("http")
async def add_metrics(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status=response.status_code).inc()
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(time.time() - start_time)
    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

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