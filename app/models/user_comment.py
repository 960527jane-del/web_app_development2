import sqlite3

DB_PATH = 'instance/database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class UserComment:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        comments = conn.execute('SELECT * FROM user_comments ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(c) for c in comments]

    @staticmethod
    def get_by_mountain_id(mountain_id):
        conn = get_db_connection()
        comments = conn.execute('''
            SELECT * FROM user_comments 
            WHERE mountain_id = ? 
            ORDER BY created_at DESC
        ''', (mountain_id,)).fetchall()
        conn.close()
        return [dict(c) for c in comments]

    @staticmethod
    def create(mountain_id, user_name, comment_content):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_comments (mountain_id, user_name, comment_content)
            VALUES (?, ?, ?)
        ''', (mountain_id, user_name, comment_content))
        conn.commit()
        comment_id = cursor.lastrowid
        conn.close()
        return comment_id

    @staticmethod
    def delete(comment_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM user_comments WHERE id = ?', (comment_id,))
        conn.commit()
        conn.close()
