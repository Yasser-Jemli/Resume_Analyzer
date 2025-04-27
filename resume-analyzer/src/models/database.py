from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        # Using SQLAlchemy connection
        self.connection = db.session
        
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        self.connect()
        result = self.connection.execute(query, params)
        return result.fetchall()

    def execute_insert(self, query, params=None):
        self.connect()
        result = self.connection.execute(query, params)
        self.connection.commit()
        return result.lastrowid