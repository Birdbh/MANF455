
from data import DatabaseManager
from data import Table

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