CREATE TABLE customers (
  customer_id SERIAL PRIMARY KEY,
  name TEXT,
  email TEXT UNIQUE,
  phone TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

COPY customers(customer_id, name, email, phone, created_at)
FROM '/docker-entrypoint-initdb.d/ofd_customers.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE addresses (
  address_id SERIAL PRIMARY KEY,
  customer_id INT,
  line1 TEXT,
  city TEXT,
  pincode TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

COPY addresses(address_id, customer_id, line1, city, pincode, created_at)
FROM '/docker-entrypoint-initdb.d/ofd_addresses.csv'
DELIMITER ','
CSV HEADER;