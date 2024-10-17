import sqlite3
from data import DatabaseConnector
from datetime import datetime
import sqlalchemy

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
                'downtimeReason TEXT NOT NULL CHECK (downtimeReason IN ("Machine Fault", "Product Malfunction", "Labour Incident")),'
                'status TEXT NOT NULL CHECK (status IN ("Pending", "Resolved"))'
                ')'
            )
            self.connection.commit()

    def add_downtime(self, employeeId: int, downtimeReason: str):
        self.connection.execute(
            'INSERT INTO downtime (employeeId, downtimeReason, status) VALUES (?, ?, ?)',
            (employeeId, downtimeReason, 'Pending')
        )
        self.connection.commit()

    def get_last_row(self):
        return self.connection.execute('SELECT * FROM downtime ORDER BY downtimeId DESC LIMIT 1').fetchone()
    
    def is_currently_downtime(self):
        return self.get_last_row_status() == 'Pending'
    
    def get_last_row_status(self):
        return self.connection.execute('SELECT status FROM downtime ORDER BY downtimeId DESC LIMIT 1').fetchone()[0]
    
    def get_last_row_reason(self):
        return self.connection.execute('SELECT downtimeReason FROM downtime ORDER BY downtimeId DESC LIMIT 1').fetchone()[0]
    
    def end_downtime(self):
        self.connection.execute('UPDATE downtime SET status = "Resolved" WHERE downtimeId = (SELECT MAX(downtimeId) FROM downtime)')
        self.connection.commit()