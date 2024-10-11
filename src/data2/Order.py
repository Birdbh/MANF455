import sqlite3
from data2 import DatabaseConnector
from datetime import datetime

class OrderTable:
    def __init__(self):
        self.connection = DatabaseConnector.Database.get_connection()
        self.create_table()

    def create_table(self):
        #check if a table called orders is in the database
        if self.connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders';").fetchone() is None:
            self.connection.execute(
                'CREATE TABLE orders ('
                'orderId INTEGER PRIMARY KEY AUTOINCREMENT,'
                'customer_id INTEGER NOT NULL,'
                'drilling_operation INTEGER NOT NULL,'
                'order_date TEXT NOT NULL,'
                'status TEXT NOT NULL,'
                'passQualityControl BOOLEAN NOT NULL'
                ')'
            )
            self.connection.commit()

    def add_order(self, customer_id: int, drilling_operation: int, order_date: str, status: str, passQualityControl: bool):
        self.connection.execute(
            'INSERT INTO orders (customer_id, drilling_operation, order_date, status, passQualityControl) VALUES (?, ?, ?, ?, ?)',
            (customer_id, drilling_operation, order_date, status, passQualityControl)
        )
        self.connection.commit()

    def get_all_orders(self):
        return self.connection.execute('SELECT * FROM orders').fetchall()
    
    def get_last_row_id(self):
        return self.connection.execute('SELECT orderId FROM orders ORDER BY orderId DESC LIMIT 1').fetchone()[0]
    
    def update_drilling_operation(self, order_id: int, new_drilling_operation: int):
        self.connection.execute('UPDATE orders SET drilling_operation = ? WHERE orderId = ?', (new_drilling_operation, order_id))
        self.connection.commit()

    def update_start_time(self, order_id: int, new_start_time: str):
        self.connection.execute('UPDATE orders SET order_date = ? WHERE orderId = ?', (new_start_time, order_id))
        self.connection.commit()

    def update_status(self, order_id: int, new_status: str):
        self.connection.execute('UPDATE orders SET status = ? WHERE orderId = ?', (new_status, order_id))
        self.connection.commit()
    
    def update_pass_quality_control(self, order_id: int, new_pass_quality_control: bool):
        self.connection.execute('UPDATE orders SET passQualityControl = ? WHERE orderId = ?', (new_pass_quality_control, order_id))
        self.connection.commit()