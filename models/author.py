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
        if hasattr(self, '_name'):
            raise AttributeError("Name cannot be changed after being initialized")
        else:
            if isinstance(new_name, str) and len(new_name) > 0:
                self._name = new_name

    def articles(self):
        """
        Returns all articles written by this author using a SQL JOIN.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT articles.id, articles.title, articles.content, articles.magazine_id
                FROM articles
                INNER JOIN authors ON articles.author_id = authors.id
                WHERE authors.id = ?
            """
            cursor.execute(sql, (self._id,))
            rows = cursor.fetchall()
            return [f"Article ID: {row[0]}, Title: {row[1]}, Content: {row[2]}, Magazine ID: {row[3]}" for row in rows] or None

    def magazines(self):
        """
        Returns all magazines where the author has published articles using SQL JOIN.
        Ensures unique magazines using DISTINCT.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT DISTINCT magazines.id, magazines.name, magazines.category
                FROM magazines
                INNER JOIN articles ON magazines.id = articles.magazine_id
                INNER JOIN authors ON articles.author_id = authors.id
                WHERE authors.id = ?
            """
            cursor.execute(sql, (self._id,))
            rows = cursor.fetchall()
            return [f"Magazine ID: {row[0]}, Name: {row[1]}, Category: {row[2]}" for row in rows] or None

    def __repr__(self):
        return f'<Author {self.name}>'
