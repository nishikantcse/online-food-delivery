# services/notification-service/app/api/main.py

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
        host="notification-db",
        database="notification_db",
        user="postgres",
        password="postgres"
    )

# 1. Send notification
@app.post("/v1/notifications")
def send_notification(payload: dict):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO notifications_log (user_id, message, type, status) VALUES (%s,%s,%s,%s)",
        (payload["user_id"], payload["message"], payload["type"], "SENT")
    )

    conn.commit()

    return {"message": "Notification sent"}

# 2. Get all notifications (pagination)
@app.get("/v1/notifications")
def get_notifications(limit: int = 10, offset: int = 0):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM notifications_log ORDER BY created_at DESC LIMIT %s OFFSET %s",
        (limit, offset)
    )

    return {"data": cur.fetchall()}

# 3. Get notifications by user
@app.get("/v1/users/{user_id}/notifications")
def get_user_notifications(user_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM notifications_log WHERE user_id=%s ORDER BY created_at DESC",
        (user_id,)
    )

    return {"data": cur.fetchall()}