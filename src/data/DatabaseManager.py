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