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
    
    @id.setter
    def id(self, id):
        if isinstance(id, int):
            self._id = id
    
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
    
    @name.setter
    def name(self, new_name):
        if hasattr(self,'_name'):
            raise AttributeError("Name cannot be changed after being initiallized")
        else:
            if isinstance(new_name, str) and len (new_name) > 0:
                self._name = new_name

    def __repr__(self):
        return f'<Author {self.name}>'
