# services/notification-service/app/api/main.py

from fastapi import FastAPI
import psycopg2

app = FastAPI()

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