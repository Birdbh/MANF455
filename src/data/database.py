import sqlite3
from typing import List, Dict, Any, Tuple

class DatabaseManager:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def execute(self, query: str, params: Tuple = None):
        if params:
            return self.cursor.execute(query, params)
        return self.cursor.execute(query)

class Table:
    def __init__(self, db_manager: DatabaseManager, table_name: str):
        self.db_manager = db_manager
        self.table_name = table_name

    def create_table(self, columns: List[str]):
        query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({', '.join(columns)})"
        with self.db_manager as db:
            db.execute(query)

    def insert(self, data: Dict[str, Any]):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        with self.db_manager as db:
            db.execute(query, tuple(data.values()))

    def select(self, conditions: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name}"
        params = ()
        if conditions:
            where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
            query += f" WHERE {where_clause}"
            params = tuple(conditions.values())
        with self.db_manager as db:
            result = db.execute(query, params).fetchall()
        return [dict(zip([column[0] for column in self.db_manager.cursor.description], row)) for row in result]

    def update(self, data: Dict[str, Any], conditions: Dict[str, Any]):
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {where_clause}"
        params = tuple(list(data.values()) + list(conditions.values()))
        with self.db_manager as db:
            db.execute(query, params)

    def delete(self, conditions: Dict[str, Any]):
        where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
        query = f"DELETE FROM {self.table_name} WHERE {where_clause}"
        with self.db_manager as db:
            db.execute(query, tuple(conditions.values()))

class Employee(Table):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager, 'employee')
        self.create_table([
            'id INTEGER PRIMARY KEY AUTOINCREMENT',
            'name TEXT NOT NULL',
            'role TEXT NOT NULL',
            'username TEXT UNIQUE NOT NULL',
            'password TEXT NOT NULL',
            'role TEXT NOT NULL CHECK (role IN ("Manager", "Technician", "Operator"))'
        ])

class Customers(Table):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager, 'customers')
        self.create_table([
            'id INTEGER PRIMARY KEY AUTOINCREMENT',
            'name TEXT NOT NULL',
            'email TEXT UNIQUE NOT NULL',
            'address TEXT'
        ])

class Orders(Table):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager, 'orders')
        self.create_table([
            'id INTEGER PRIMARY KEY AUTOINCREMENT',
            'customer_id INTEGER NOT NULL',
            'employee_id INTEGER NOT NULL',
            'order_date TEXT NOT NULL',
            'status TEXT NOT NULL',
            'FOREIGN KEY (customer_id) REFERENCES customers (id)',
            'FOREIGN KEY (employee_id) REFERENCES employee (id)'
        ])

class MESDatabase:
    def __init__(self, db_name: str):
        self.db_manager = DatabaseManager(db_name)
        self.employees = Employee(self.db_manager)
        self.customers = Customers(self.db_manager)
        self.orders = Orders(self.db_manager)

# # Usage example:
# if __name__ == "__main__":
#     db = MESDatabase("mes.db")

#     # Adding an operator
#     db.operators.insert({
#         'name': 'John Doe',
#         'role': 'Technician',
#         'username': 'john.doe',
#         'password': 'hashed_password_here'
#     })

#     # Adding a customer
#     db.customers.insert({
#         'name': 'Acme Corp',
#         'email': 'contact@acmecorp.com',
#         'address': '123 Main St, City, Country'
#     })

#     # Adding an order
#     db.orders.insert({
#         'customer_id': 1,
#         'operator_id': 1,
#         'order_date': '2024-10-08',
#         'status': 'Pending'
#     })

#     # Querying data
#     operators = db.operators.select({'role': 'Technician'})
#     print("Technicians:", operators)

#     customers = db.customers.select({'name': 'Acme Corp'})
#     print("Acme Corp customer:", customers)

#     orders = db.orders.select({'status': 'Pending'})
#     print("Pending orders:", orders)

#     # Updating data
#     db.orders.update({'status': 'In Progress'}, {'id': 1})

#     # Deleting data
#     db.customers.delete({'id': 1})