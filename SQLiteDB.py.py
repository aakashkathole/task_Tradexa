
# Simultaneous insert operations into three separate SQLite databases using threads.

# importing SQLite DB  module
import sqlite3
import threading

# Create three models
# users model
users_data = [
    (1, 'Alice', 'alice@example.com'),
    (2, 'Bob', 'bob@example.com'),
    (3, 'Charlie', 'charlie@example.com'),
    (4, 'David', 'david@example.com'),
    (5, 'Eve', 'eve@example.com'),
    (6, 'Frank', 'frank@example.com'),
    (7, 'Grace', 'grace@example.com'),
    (8, 'Alice', 'alice@example.com'),
    (9, 'Henry', 'henry@example.com'),
    (10, '', 'jane@example.com')
]

# products model
products_data = [
    (1, 'Laptop', 1000.00),
    (2, 'Smartphone', 700.00),
    (3, 'Headphones', 150.00),
    (4, 'Monitor', 300.00),
    (5, 'Keyboard', 50.00),
    (6, 'Mouse', 30.00),
    (7, 'Laptop', 1000.00),
    (8, 'Smartwatch', 250.00),
    (9, 'Gaming Chair', 500.00),
    (10, 'Earbuds', -50.00)  # Invalid price
]

# orders model
orders_data = [
    (1, 1, 1, 2),
    (2, 2, 2, 1),
    (3, 3, 3, 5),
    (4, 4, 4, 1),
    (5, 5, 5, 3),
    (6, 6, 6, 4),
    (7, 7, 7, 2),
    (8, 8, 8, 0),  # Invalid quantity
    (9, 9, 1, -1),  # Invalid quantity
    (10, 10, 11, 2)  # Invalid product_id
]

# Function to insert users model into users DB
def insert_users():
    print("Starting user insertion...")
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, email TEXT)')
    for user in users_data:
        try:
            cursor.execute('INSERT INTO users (id, name, email) VALUES (?, ?, ?)', user)
            print(f"Inserted user: {user[1]}")
        except sqlite3.IntegrityError as e:
            print(f"Error inserting user {user[1]}: {e}")
    conn.commit()
    conn.close()

# Function to insert products model into products DB
def insert_products():
    print("Starting product insertion...")
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER, name TEXT, price REAL)')
    for product in products_data:
        try:
            if product[2] < 0:
                print(f"Skipping product {product[1]} with invalid price: {product[2]}")
                continue
            cursor.execute('INSERT INTO products (id, name, price) VALUES (?, ?, ?)', product)
            print(f"Inserted product: {product[1]} with price {product[2]}")
        except sqlite3.IntegrityError as e:
            print(f"Error inserting product {product[1]}: {e}")
    conn.commit()
    conn.close()

# Function to insert orders model into Orders DB
def insert_orders():
    print("Starting order insertion...")
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER, user_id INTEGER, product_id INTEGER, quantity INTEGER)')
    for order in orders_data:
        try:
            if order[3] <= 0:
                print(f"Skipping order {order[0]} with invalid quantity: {order[3]}")
                continue
            cursor.execute('INSERT INTO orders (id, user_id, product_id, quantity) VALUES (?, ?, ?, ?)', order)
            print(f"Inserted order {order[0]} for user {order[1]} and product {order[2]} with quantity {order[3]}")
        except sqlite3.IntegrityError as e:
            print(f"Error inserting order {order[0]}: {e}")
    conn.commit()
    conn.close()

# Function to run all insertions threads
def run_insertions():
    threads = []
    
    # Create threads for all models
    threads.append(threading.Thread(target=insert_users))
    threads.append(threading.Thread(target=insert_products))
    threads.append(threading.Thread(target=insert_orders))
    
    # Start threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Print message
    print("All insertions completed.")

# Run insertion
run_insertions()