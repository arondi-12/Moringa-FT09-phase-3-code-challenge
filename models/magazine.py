from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name = None, category = None):
        self._id = id
        self._name = name
        self._category = category

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO magazine (name, category) VALUES (?,?)",
        (self.name, self.category)
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
            (self._id, self._name, self._category)
        )
        self._name = cursor.fetchone()[0]
        conn.close()
        return self._name
    
    @id.setter
    def id(self,id):
        if isinstance(id, int):
            self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if isinstance(new_name, int) and 2 <= len (new_name) <= 16:
            self._name = new_name

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, new_category):
        if isinstance(new_category, str) and len (new_category) > 0:
            self._category = new_category


    def __repr__(self):
        return f'<Magazine {self.name} {self.id} {self.category}>'
