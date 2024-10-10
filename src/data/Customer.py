from data import DatabaseManager
from data import Table

class Customers(Table):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager, 'customers')
        self.create_table([
            'id INTEGER PRIMARY KEY AUTOINCREMENT',
            'name TEXT NOT NULL',
            'email TEXT UNIQUE NOT NULL',
            'address TEXT'
        ])