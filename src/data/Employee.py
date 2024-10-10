
from data import DatabaseManager
from data import Table

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