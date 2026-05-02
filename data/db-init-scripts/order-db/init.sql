CREATE TABLE orders (
  order_id INT PRIMARY KEY,
  customer_id INT,
  restaurant_id INT,
  address_id INT,
  order_status TEXT,
  order_total FLOAT,
  payment_status TEXT,
  created_at TIMESTAMP
);

COPY orders(order_id, customer_id, restaurant_id, address_id, order_status, order_total, payment_status, created_at)
FROM '/docker-entrypoint-initdb.d/ofd_orders.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE order_items (
  order_item_id INT PRIMARY KEY,
  order_id INT,
  item_id INT,
  quantity INT,
  price FLOAT
);

COPY order_items(order_item_id, order_id, item_id, quantity, price)
FROM '/docker-entrypoint-initdb.d/ofd_order_items.csv'
DELIMITER ','
CSV HEADER;