import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        #still need to determine table structure
        self.cur.execute("")
        self.conn.commit()

    def fetch(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows
    
    def insert(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def close(self):
        self.conn.close()