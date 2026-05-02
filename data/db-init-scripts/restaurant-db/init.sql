CREATE TABLE restaurants (
  restaurant_id INT PRIMARY KEY,
  name TEXT,
  cuisine TEXT,
  city TEXT,
  rating FLOAT,
  is_open BOOLEAN,
  created_at TIMESTAMP
);

COPY restaurants(restaurant_id, name, cuisine, city, rating, is_open, created_at)
FROM '/docker-entrypoint-initdb.d/ofd_restaurants.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE menu_items (
  item_id INT PRIMARY KEY,
  restaurant_id INT,
  name TEXT,
  category TEXT,
  price FLOAT,
  is_available BOOLEAN
);

COPY menu_items(item_id, restaurant_id, name, category, price, is_available)
FROM '/docker-entrypoint-initdb.d/ofd_menu_items.csv'
DELIMITER ','
CSV HEADER;