import sqlite3
from typing import List, Dict, Any, Tuple

from data import DatabaseManager

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