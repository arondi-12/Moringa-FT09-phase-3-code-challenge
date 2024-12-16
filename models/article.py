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
            "INSERT INTO articles (title) VALUES (?)"
            (title)
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


    def __repr__(self):
        return f'<Article {self.title}>'
