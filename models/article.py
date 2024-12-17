from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self._id = id
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
            (title, content, author_id, magazine_id)
        )

        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    @property
    def author(self):
        """
        Returns the author of the article using a SQL JOIN.
        """
        from models.author import Author
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT authors.*
                FROM authors
                INNER JOIN articles ON authors.id = articles.author_id
                WHERE articles.id = ?
            """
            cursor.execute(sql, (self._id,))
            author_data = cursor.fetchone()
            
            if author_data:
                return Author(*author_data)  
            return None

    @property
    def magazine(self):
        """
        Returns the magazine in which the article is published using a SQL JOIN.
        """
        from models.magazine import Magazine
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT magazines.*
                FROM magazines
                INNER JOIN articles ON magazines.id = articles.magazine_id
                WHERE articles.id = ?
            """
            cursor.execute(sql, (self._id,))
            magazine_data = cursor.fetchone()
            
            if magazine_data:
                return Magazine(*magazine_data)  
            return None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        if hasattr(self, '_title'):
            raise AttributeError("Title cannot be changed after being initialized")
        else:
            if isinstance(new_title, str) and 5 <= len(new_title) <= 50:
                self._title = new_title
            else:
                raise ValueError("Title must be a non-empty string between 5 and 50 characters")

    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, content):
        if isinstance(content, str) and len(content):
            self._content = content
        else:
            raise ValueError("Content must be a non-empty string")

    def __repr__(self):
        return f'<Article {self.title}>'
