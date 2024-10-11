import sqlite3
from data2 import DatabaseConnector
from datetime import datetime

class DowntimeTable:
    def __init__(self):
        self.connection = DatabaseConnector.Database.get_connection()
        self.create_table()

    def create_table(self):
        #check if a table called orders is in the database
        if self.connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='downtime';").fetchone() is None:
            self.connection.execute(
                'CREATE TABLE downtime ('
                'downtimeId INTEGER PRIMARY KEY AUTOINCREMENT,'
                'employeeId INTEGER NOT NULL,'
                'downtimeReason Text NOT NULL,'
                'status TEXT NOT NULL CHECK (status IN ("Machine Fault", "Product Malfunction", "Labour Incident"))'
                ')'
            )
            self.connection.commit()

    def add_downtime(self, employeeId: int, downtimeReason: str, status: str):
        self.connection.execute(
            'INSERT INTO downtime (employeeId, downtimeReason, status) VALUES (?, ?, ?)',
            (employeeId, downtimeReason, status)
        )
        self.connection.commit()