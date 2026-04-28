-- 山岳基本資料表
CREATE TABLE IF NOT EXISTS mountains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    altitude INTEGER,
    location TEXT,
    description TEXT,
    safety_warning TEXT,
    equipment_list TEXT,
    trail_timeline TEXT
);

-- 使用者評論表
CREATE TABLE IF NOT EXISTS user_comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mountain_id INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    comment_content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mountain_id) REFERENCES mountains(id) ON DELETE CASCADE
);
