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
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        if hasattr(self,'_title'):
            raise AttributeError("Name cannot be changed after being initiallized")
        else:
            if isinstance(new_title, str) and len (new_title) >= 5 and len(new_title) <= 50:
                self._title = new_title

            else:
                raise ValueError("Title must be a non-empty string")

    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, content):
        if isinstance(content, str) and len(content):
            self._content = content
        else:
            raise ValueError(
                "Content must be a non-empty string"
            )
        
    @property
    def author_id(self):
        return self._author_id
    
    @author_id.setter
    def author_id(self, author_id):
        from models.author import Author
        if type(author_id) is int and Author.find_by_id(author_id):
            self._author_id = author_id
        else:
            raise ValueError(
                "Author ID should match the database")
        
    @property
    def magazine_id(self):
        return self._magazine_id
    
    @magazine_id.setter
    def magazine_id(self, magazine_id):
        from models.magazine import Magazine
        if type(magazine_id) is int and Magazine.find_by_id(magazine_id):
            self._magazine_id = magazine_id
        else:
            raise ValueError("Magazine ID must match a magazine in the database")
    def author(self):
        from models.author import Author
        conn = get_db_connection()
        CURSOR = conn.cursor()
        """retrieves and returns the author who wrote this article"""
        sql = """
            SELECT a.*
            FROM authors a
            INNER JOIN articles ar ON ar.author = a.id
            WHERE ar.id = ?
        """
        CURSOR.execute(sql, (self.id))
        author_data = CURSOR.fetchone()

        if author_data:
            return Author(*author_data)
        else:
            return None

    def magazine(self):
        from models.magazine import Magazine
        conn = get_db_connection()
        CURSOR = conn.cursor()
        """retrieves and returns the magazine in which this article is published"""
        sql = """
            SELECT m.*
            FROM magazines m
            INNER JOIN articles ar ON ar.magazine = m.id
            WHERE ar.id = ?
        """
        CURSOR.execute(sql, (self.id))
        magazine_data = CURSOR.fetchone()

        if magazine_data:
            return Magazine(*magazine_data)
        else:
            return None  


    def __repr__(self):
        return f'<Article {self.title}>'
