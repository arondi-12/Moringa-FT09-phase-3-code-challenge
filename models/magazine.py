from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name = None, category = None):
        self._id = id
        self._name = name
        self._category = category if category is not None else "Uncategorized"

        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO magazines (name, category)
            VALUES (?,?)
        """
        cursor.execute(sql, (self._name, self._category))
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id
    
    
    
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