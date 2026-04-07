CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    signup_date DATE NOT NULL
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INTEGER,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    status TEXT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    order_date DATE NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);

-- Seed Data
INSERT INTO users (id, name, email, signup_date) VALUES 
(1, 'Alice Smith', 'alice@example.com', '2023-01-10'),
(2, 'Bob Jones', 'bob@example.com', '2023-02-15'),
(3, 'Charlie Brown', 'charlie@example.com', '2023-03-20'),
(4, 'Diana Prince', 'diana@example.com', '2023-04-25');

INSERT INTO categories (id, name) VALUES 
(1, 'Electronics'),
(2, 'Clothing'),
(3, 'Home & Garden');

INSERT INTO products (id, name, category_id, price) VALUES 
(1, 'Laptop', 1, 999.99),
(2, 'Smartphone', 1, 499.99),
(3, 'T-Shirt', 2, 19.99),
(4, 'Jeans', 2, 49.99),
(5, 'Coffee Maker', 3, 79.99),
(6, 'Blender', 3, 39.99);

INSERT INTO orders (id, user_id, status, total_amount, order_date) VALUES 
(1, 1, 'COMPLETED', 1019.98, '2023-05-01'),
(2, 2, 'PENDING', 49.99, '2023-05-02'),
(3, 3, 'COMPLETED', 89.98, '2023-05-03'),
(4, 1, 'COMPLETED', 499.99, '2023-06-01'),
(5, 4, 'PENDING', 19.99, '2023-06-02');

INSERT INTO order_items (id, order_id, product_id, quantity, unit_price) VALUES 
(1, 1, 1, 1, 999.99),
(2, 1, 3, 1, 19.99),
(3, 2, 4, 1, 49.99),
(4, 3, 5, 1, 79.99),
(5, 4, 2, 1, 499.99),
(6, 5, 3, 1, 19.99);
