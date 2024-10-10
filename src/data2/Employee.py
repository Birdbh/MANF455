import sqlite3
from data2 import DatabaseConnector

class EmployeeTable:
    def __init__(self):
        self.connection = DatabaseConnector.Database.get_connection()
        self.create_table()

    def create_table(self):
        #check if a table called orders is in the database
        if self.connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employee';").fetchone() is None:
            self.connection.execute(
                'CREATE TABLE employee ('
                'employeeId INTEGER PRIMARY KEY AUTOINCREMENT,'
                'name TEXT NOT NULL,'
                'username TEXT UNIQUE NOT NULL,'
                'password TEXT NOT NULL,'
                'role TEXT NOT NULL CHECK (role IN ("Manager", "Technician", "Operator"))'
                ')'
            )
            self.connection.commit()

    def add_employee(self, name: str, username: str, password: str, role: str,):
        self.connection.execute(
            'INSERT INTO employee (name, username, password, role) VALUES (?, ?, ?, ?)',
            (name, username, password, role)
        )
        self.connection.commit()

    def get_all_employees(self):
        return self.connection.execute('SELECT * FROM employee').fetchall()
    
    def get_all_operators(self):
        return self.connection.execute('SELECT * FROM employee WHERE role = "Operator"').fetchall()
    
    def validate_user(self, username, password):
        query_results = self.connection.execute('SELECT * FROM employee WHERE username = ? AND password = ?', (username, password)).fetchone()
        if query_results is not None:
            #return the role of the user
            return query_results[4]
