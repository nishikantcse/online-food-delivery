CREATE TABLE payments (
  payment_id INT PRIMARY KEY,
  order_id INT,
  amount FLOAT,
  method TEXT,
  status TEXT,
  reference TEXT,
  created_at TIMESTAMP
);

COPY payments(payment_id, order_id, amount, method, status, reference, created_at)
FROM '/docker-entrypoint-initdb.d/ofd_payments.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE idempotency_keys (
  id SERIAL PRIMARY KEY,
  idempotency_key TEXT UNIQUE,
  response TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);