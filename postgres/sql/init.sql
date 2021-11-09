CREATE TABLE etl.orders (
  order_id INTEGER PRIMARY KEY,
  product_id INTEGER NOT NULL,
  customer_id INTEGER NOT NULL,
  order_state VARCHAR(70) NOT NULL,
  order_date VARCHAR(70) NOT NULL,
  order_quantity INTEGER NOT NULL
);
