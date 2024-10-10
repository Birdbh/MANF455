import sqlite3
from data2 import DatabaseConnector

class OrderTable:
    def __init__(self):
        self.connection = DatabaseConnector.Database.get_connection()
        self.create_table()

    def create_table(self):
        #check if a table called orders is in the database
        if self.connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders';").fetchone() is None:
            self.connection.execute(
                'CREATE TABLE orders ('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'customer_id INTEGER NOT NULL,'
                'employee_id INTEGER NOT NULL,'
                'order_date TEXT NOT NULL,'
                'status TEXT NOT NULL,'
                'FOREIGN KEY (customer_id) REFERENCES customers (id),'
                'FOREIGN KEY (employee_id) REFERENCES employee (id)'
                ')'
            )
            self.connection.commit()

    def add_order(self, customer_id: int, employee_id: int, order_date: str, status: str):
        self.connection.execute(
            'INSERT INTO orders (customer_id, employee_id, order_date, status) VALUES (?, ?, ?, ?)',
            (customer_id, employee_id, order_date, status)
        )
        self.connection.commit()

    def get_all_orders(self):
        return self.connection.execute('SELECT * FROM orders').fetchall()