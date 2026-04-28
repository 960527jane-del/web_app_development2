import sqlite3
import os

def get_db_connection():
    """建立並回傳資料庫連線"""
    db_path = os.path.join('instance', 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

class UserComment:
    @staticmethod
    def get_all():
        """取得所有評論記錄"""
        try:
            with get_db_connection() as conn:
                comments = conn.execute('SELECT * FROM user_comments ORDER BY created_at DESC').fetchall()
                return [dict(c) for c in comments]
        except sqlite3.Error as e:
            print(f"Database error in get_all: {e}")
            return []

    @staticmethod
    def get_by_id(comment_id):
        """根據 ID 取得單筆評論"""
        try:
            with get_db_connection() as conn:
                comment = conn.execute('SELECT * FROM user_comments WHERE id = ?', (comment_id,)).fetchone()
                return dict(comment) if comment else None
        except sqlite3.Error as e:
            print(f"Database error in get_by_id: {e}")
            return None

    @staticmethod
    def get_by_mountain_id(mountain_id):
        """取得特定山岳的所有評論"""
        try:
            with get_db_connection() as conn:
                comments = conn.execute('''
                    SELECT * FROM user_comments 
                    WHERE mountain_id = ? 
                    ORDER BY created_at DESC
                ''', (mountain_id,)).fetchall()
                return [dict(c) for c in comments]
        except sqlite3.Error as e:
            print(f"Database error in get_by_mountain_id: {e}")
            return []

    @staticmethod
    def create(data):
        """
        新增一筆評論記錄
        :param data: dict 包含 mountain_id, user_name, comment_content
        :return: int 新增的記錄 ID，失敗回傳 None
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO user_comments (mountain_id, user_name, comment_content)
                    VALUES (?, ?, ?)
                ''', (
                    data.get('mountain_id'), 
                    data.get('user_name'), 
                    data.get('comment_content')
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in create: {e}")
            return None

    @staticmethod
    def update(comment_id, data):
        """
        更新一筆評論記錄
        :param comment_id: int 評論 ID
        :param data: dict 包含要更新的欄位與值
        :return: bool 是否更新成功
        """
        if not data:
            return False
            
        try:
            with get_db_connection() as conn:
                set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
                values = list(data.values())
                values.append(comment_id)
                
                conn.execute(f'UPDATE user_comments SET {set_clause} WHERE id = ?', values)
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in update: {e}")
            return False

    @staticmethod
    def delete(comment_id):
        """刪除一筆評論記錄"""
        try:
            with get_db_connection() as conn:
                conn.execute('DELETE FROM user_comments WHERE id = ?', (comment_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in delete: {e}")
            return False
