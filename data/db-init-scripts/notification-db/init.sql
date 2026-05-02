CREATE TABLE notifications_log (
  id SERIAL PRIMARY KEY,
  user_id INT,
  message TEXT,
  type TEXT,
  status TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);