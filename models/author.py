from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO authors (name) VALUES (?)",
            (name,)
        )
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM authors WHERE id = ?",
            (self._id,)
        )
        self._name = cursor.fetchone()[0]
        conn.close()
        return self._name

    def __repr__(self):
        return f'<Author {self.name}>'
