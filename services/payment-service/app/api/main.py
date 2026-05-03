# services/payment-service/app/api/main.py

from fastapi import FastAPI, HTTPException, Request, Response, Header
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