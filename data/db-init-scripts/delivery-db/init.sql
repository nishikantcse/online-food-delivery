CREATE TABLE drivers (
  driver_id INT PRIMARY KEY,
  name TEXT,
  phone TEXT,
  vehicle_type TEXT,
  is_active BOOLEAN
);

CREATE TABLE deliveries (
  delivery_id INT PRIMARY KEY,
  order_id INT,
  driver_id INT,
  status TEXT,
  assigned_at TIMESTAMP,
  picked_at TIMESTAMP,
  delivered_at TIMESTAMP
);