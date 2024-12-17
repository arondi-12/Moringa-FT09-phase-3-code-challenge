from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name=None, category=None):
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
    def id(self, id):
        if isinstance(id, int):
            self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and 2 <= len(new_name) <= 16:
            self._name = new_name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if isinstance(new_category, str) and len(new_category) > 0:
            self._category = new_category

    def __repr__(self):
        return f'<Magazine {self.name} {self.id} {self.category}>'

    def articles(self):
        """
        Returns all articles associated with this magazine using a JOIN.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT articles.id, articles.title, articles.content, articles.author_id 
                FROM articles
                INNER JOIN magazines ON articles.magazine_id = magazines.id
                WHERE magazines.id = ?
            """
            cursor.execute(sql, (self._id,))
            rows = cursor.fetchall()
            return [f"Article ID: {row[0]}, Title: {row[1]}, Content: {row[2]}, Author ID: {row[3]}" for row in rows]

    def contributors(self):
        """
        Returns all authors who have written articles for this magazine.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT DISTINCT authors.id, authors.name
                FROM authors
                INNER JOIN articles ON authors.id = articles.author_id
                INNER JOIN magazines ON articles.magazine_id = magazines.id
                WHERE magazines.id = ?
            """
            cursor.execute(sql, (self._id,))
            rows = cursor.fetchall()
            return [f"Author ID: {row[0]}, Name: {row[1]}" for row in rows]

    def article_titles(self):
        """
        Returns a list of titles of all articles written for this magazine.
        Returns None if the magazine has no articles.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT articles.title
                FROM articles
                WHERE articles.magazine_id = ?
            """
            cursor.execute(sql, (self._id,))
            rows = cursor.fetchall()
            if rows:
                return [row[0] for row in rows]
            return None

    def contributing_authors(self):
        """
        Returns a list of authors who have written more than 2 articles for this magazine.
        Returns None if no authors meet the criteria.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT authors.id, authors.name
                FROM authors
                INNER JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id = ?
                GROUP BY authors.id
                HAVING COUNT(articles.id) > 2
            """
            cursor.execute(sql, (self._id,))
            rows = cursor.fetchall()
            if rows:
                return [f"Author ID: {row[0]}, Name: {row[1]}" for row in rows]
            return None
