import sqlite3
from datetime import datetime
from config import DATABASE_PATH


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # جدول کاربران
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                join_date TIMESTAMP,
                score INTEGER DEFAULT 0,
                is_blocked BOOLEAN DEFAULT 0,
                last_activity TIMESTAMP
            )
        ''')

        # جدول پیام‌ها
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message_text TEXT,
                bot_response TEXT,
                timestamp TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        # جدول بازی‌ها
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                game_type TEXT,
                score INTEGER,
                timestamp TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        # جدول محتوای قابل مدیریت
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_type TEXT,
                title TEXT,
                body TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')

        self.conn.commit()

    def add_user(self, user_id, username, first_name, last_name):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, join_date, last_activity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, datetime.now(), datetime.now()))
        self.conn.commit()

    def get_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()

    def update_score(self, user_id, score):
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE users SET score = score + ? WHERE user_id = ?', (score, user_id))
        self.conn.commit()

    def get_top_users(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT user_id, username, first_name, score FROM users ORDER BY score DESC LIMIT ?', (limit,))
        return cursor.fetchall()

    def save_message(self, user_id, message_text, bot_response):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO messages (user_id, message_text, bot_response, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (user_id, message_text, bot_response, datetime.now()))
        self.conn.commit()

    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT user_id, username, first_name FROM users WHERE is_blocked = 0')
        return cursor.fetchall()

    def block_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE users SET is_blocked = 1 WHERE user_id = ?', (user_id,))
        self.conn.commit()

    def unblock_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE users SET is_blocked = 0 WHERE user_id = ?', (user_id,))
        self.conn.commit()


db = Database()
