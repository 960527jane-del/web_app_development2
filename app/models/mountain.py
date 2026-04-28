import sqlite3
import os

def get_db_connection():
    """建立並回傳資料庫連線"""
    db_path = os.path.join('instance', 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

class Mountain:
    @staticmethod
    def get_all():
        """取得所有山岳記錄"""
        try:
            with get_db_connection() as conn:
                mountains = conn.execute('SELECT * FROM mountains').fetchall()
                return [dict(m) for m in mountains]
        except sqlite3.Error as e:
            print(f"Database error in get_all: {e}")
            return []

    @staticmethod
    def get_by_id(mountain_id):
        """根據 ID 取得單筆山岳記錄"""
        try:
            with get_db_connection() as conn:
                mountain = conn.execute('SELECT * FROM mountains WHERE id = ?', (mountain_id,)).fetchone()
                return dict(mountain) if mountain else None
        except sqlite3.Error as e:
            print(f"Database error in get_by_id: {e}")
            return None

    @staticmethod
    def search(keyword):
        """根據關鍵字搜尋山岳名稱或位置"""
        try:
            with get_db_connection() as conn:
                query = "SELECT * FROM mountains WHERE name LIKE ? OR location LIKE ?"
                mountains = conn.execute(query, (f'%{keyword}%', f'%{keyword}%')).fetchall()
                return [dict(m) for m in mountains]
        except sqlite3.Error as e:
            print(f"Database error in search: {e}")
            return []

    @staticmethod
    def create(data):
        """
        新增一筆山岳記錄
        :param data: dict 包含 name, altitude, location, description, safety_warning, equipment_list, trail_timeline
        :return: int 新增的記錄 ID，失敗回傳 None
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO mountains (name, altitude, location, description, safety_warning, equipment_list, trail_timeline)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data.get('name'), 
                    data.get('altitude'), 
                    data.get('location'), 
                    data.get('description'), 
                    data.get('safety_warning'), 
                    data.get('equipment_list'), 
                    data.get('trail_timeline')
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in create: {e}")
            return None

    @staticmethod
    def update(mountain_id, data):
        """
        更新一筆山岳記錄
        :param mountain_id: int 山岳 ID
        :param data: dict 包含要更新的欄位與值
        :return: bool 是否更新成功
        """
        if not data:
            return False
            
        try:
            with get_db_connection() as conn:
                set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
                values = list(data.values())
                values.append(mountain_id)
                
                conn.execute(f'UPDATE mountains SET {set_clause} WHERE id = ?', values)
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in update: {e}")
            return False

    @staticmethod
    def delete(mountain_id):
        """刪除一筆山岳記錄"""
        try:
            with get_db_connection() as conn:
                conn.execute('DELETE FROM mountains WHERE id = ?', (mountain_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in delete: {e}")
            return False
