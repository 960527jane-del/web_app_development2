import sqlite3

DB_PATH = 'instance/database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Mountain:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        mountains = conn.execute('SELECT * FROM mountains').fetchall()
        conn.close()
        return [dict(m) for m in mountains]

    @staticmethod
    def get_by_id(mountain_id):
        conn = get_db_connection()
        mountain = conn.execute('SELECT * FROM mountains WHERE id = ?', (mountain_id,)).fetchone()
        conn.close()
        return dict(mountain) if mountain else None

    @staticmethod
    def search(keyword):
        conn = get_db_connection()
        query = "SELECT * FROM mountains WHERE name LIKE ? OR location LIKE ?"
        mountains = conn.execute(query, (f'%{keyword}%', f'%{keyword}%')).fetchall()
        conn.close()
        return [dict(m) for m in mountains]

    @staticmethod
    def create(name, altitude, location, description, safety_warning, equipment_list, trail_timeline):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mountains (name, altitude, location, description, safety_warning, equipment_list, trail_timeline)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, altitude, location, description, safety_warning, equipment_list, trail_timeline))
        conn.commit()
        mountain_id = cursor.lastrowid
        conn.close()
        return mountain_id

    @staticmethod
    def update(mountain_id, **kwargs):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(mountain_id)
        
        cursor.execute(f'''
            UPDATE mountains SET {set_clause} WHERE id = ?
        ''', values)
        conn.commit()
        conn.close()

    @staticmethod
    def delete(mountain_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM mountains WHERE id = ?', (mountain_id,))
        conn.commit()
        conn.close()
