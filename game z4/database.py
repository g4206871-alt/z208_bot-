import sqlite3
import json
from datetime import datetime
from config import DATABASE_PATH


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # برای دسترسی به ستون‌ها با اسم
        self.conn.execute("PRAGMA journal_mode=WAL")  # افزایش سرعت
        self.conn.execute("PRAGMA foreign_keys = ON")  # فعال کردن کلید خارجی
        self.create_tables()

    def create_tables(self):
        """ساخت تمام جداول با ساختار پیشرفته"""
        cursor = self.conn.cursor()

        # ============ جدول کاربران با اطلاعات کامل ============
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                full_name TEXT,
                language_code TEXT,
                is_premium BOOLEAN DEFAULT 0,
                phone_number TEXT,
                bio TEXT,
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                first_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_messages INTEGER DEFAULT 0,
                total_interactions INTEGER DEFAULT 0,
                score INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                experience INTEGER DEFAULT 0,
                is_blocked BOOLEAN DEFAULT 0,
                is_admin BOOLEAN DEFAULT 0,
                current_state TEXT DEFAULT 'normal',
                preferences TEXT DEFAULT '{}',
                metadata TEXT DEFAULT '{}',
                session_count INTEGER DEFAULT 0,
                achievements TEXT DEFAULT '[]',
                badges TEXT DEFAULT '[]'
            )
        ''')

        # ============ جدول پیام‌ها با حافظه کامل ============
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message_text TEXT,
                bot_response TEXT,
                message_type TEXT DEFAULT 'text',
                chat_type TEXT DEFAULT 'private',
                intent TEXT,
                sentiment TEXT,
                tokens_count INTEGER DEFAULT 0,
                response_time REAL DEFAULT 0,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT,
                is_edited BOOLEAN DEFAULT 0,
                is_deleted BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')

        # ============ جدول تاریخچه گفتگو ============
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_id TEXT NOT NULL,
                messages_json TEXT DEFAULT '[]',
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                total_exchanges INTEGER DEFAULT 0,
                topics_discussed TEXT DEFAULT '[]',
                user_mood TEXT DEFAULT 'neutral',
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')

        # ============ جدول حافظه کاربر ============
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                remembered_facts TEXT DEFAULT '{}',
                preferences TEXT DEFAULT '{}',
                interaction_patterns TEXT DEFAULT '{}',
                favorite_topics TEXT DEFAULT '[]',
                personality_traits TEXT DEFAULT '{}',
                learning_style TEXT DEFAULT 'visual',
                interests TEXT DEFAULT '[]',
                language_level TEXT DEFAULT 'intermediate',
                last_topics TEXT DEFAULT '[]',
                custom_data TEXT DEFAULT '{}',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')

        # ============ جدول دستاوردها ============
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                achievement_key TEXT NOT NULL,
                achievement_name TEXT NOT NULL,
                achievement_desc TEXT,
                icon TEXT DEFAULT '🏆',
                earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notified BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                UNIQUE(user_id, achievement_key)
            )
        ''')

        # ============ جدول جلسات کاربر ============
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_id TEXT UNIQUE NOT NULL,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                duration INTEGER DEFAULT 0,
                messages_sent INTEGER DEFAULT 0,
                features_used TEXT DEFAULT '[]',
                device_info TEXT DEFAULT '{}',
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')

        # ============ جدول لاگ فعالیت‌ها ============
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                action_type TEXT DEFAULT 'interaction',
                details TEXT DEFAULT '{}',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')

        # ============ جدول نوتیفیکیشن‌ها ============
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                notification_type TEXT DEFAULT 'info',
                is_read BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                read_at TIMESTAMP,
                action_url TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')

        # ============ جدول آمار روزانه ============
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                total_users INTEGER DEFAULT 0,
                new_users INTEGER DEFAULT 0,
                active_users INTEGER DEFAULT 0,
                total_messages INTEGER DEFAULT 0,
                ai_queries INTEGER DEFAULT 0,
                anime_views INTEGER DEFAULT 0,
                support_tickets INTEGER DEFAULT 0,
                ratings_given INTEGER DEFAULT 0,
                average_rating REAL DEFAULT 0,
                peak_hour INTEGER DEFAULT 0,
                metadata TEXT DEFAULT '{}',
                UNIQUE(date)
            )
        ''')

        # ============ ایندکس‌ها برای سرعت ============
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_history_user ON chat_history(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_activity_user ON activity_log(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_achievements_user ON achievements(user_id)')

        self.conn.commit()

    # ============ متدهای پیشرفته کاربران ============

    def add_or_update_user(self, user_id, username=None, first_name=None, 
                           last_name=None, language_code=None, is_premium=False):
        """اضافه کردن یا بروزرسانی کامل اطلاعات کاربر"""
        cursor = self.conn.cursor()
        now = datetime.now()

        # بررسی وجود کاربر
        existing = self.get_user(user_id)

        if existing:
            # بروزرسانی کاربر موجود
            cursor.execute('''
                UPDATE users SET 
                    username = COALESCE(?, username),
                    first_name = COALESCE(?, first_name),
                    last_name = COALESCE(?, last_name),
                    full_name = ?,
                    language_code = COALESCE(?, language_code),
                    is_premium = ?,
                    last_activity = ?,
                    total_interactions = total_interactions + 1
                WHERE user_id = ?
            ''', (
                username, first_name, last_name,
                f"{first_name or ''} {last_name or ''}".strip() or None,
                language_code, is_premium, now, user_id
            ))
        else:
            # ایجاد کاربر جدید
            full_name = f"{first_name or ''} {last_name or ''}".strip() or None
            cursor.execute('''
                INSERT INTO users (
                    user_id, username, first_name, last_name, full_name,
                    language_code, is_premium, join_date, first_interaction,
                    last_activity, total_interactions, session_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, username, first_name, last_name, full_name,
                language_code, is_premium, now, now, now, 1, 1
            ))

        self.conn.commit()
        return self.get_user(user_id)

    def get_user(self, user_id):
        """دریافت کامل اطلاعات کاربر"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_user_activity(self, user_id):
        """بروزرسانی آخرین فعالیت کاربر"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE users SET 
                last_activity = ?,
                total_interactions = total_interactions + 1
            WHERE user_id = ?
        ''', (datetime.now(), user_id))
        self.conn.commit()

    def get_user_score(self, user_id):
        """دریافت امتیاز کاربر"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT score FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result['score'] if result else 0

    def update_score(self, user_id, score):
        """افزایش امتیاز کاربر"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE users SET 
                score = score + ?,
                experience = experience + ?,
                last_activity = ?
            WHERE user_id = ?
        ''', (score, score, datetime.now(), user_id))
        self.conn.commit()
        self._check_level_up(user_id)

    def _check_level_up(self, user_id):
        """بررسی ارتقاء سطح کاربر"""
        user = self.get_user(user_id)
        if user:
            new_level = (user['experience'] // 100) + 1
            if new_level > user['level']:
                cursor = self.conn.cursor()
                cursor.execute('UPDATE users SET level = ? WHERE user_id = ?',
                             (new_level, user_id))
                self.conn.commit()
                return new_level
        return None

    def get_top_users(self, limit=10):
        """دریافت کاربران برتر"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT user_id, username, first_name, last_name, score, level
            FROM users 
            WHERE is_blocked = 0 
            ORDER BY score DESC 
            LIMIT ?
        ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]

    def get_user_rank(self, user_id):
        """دریافت رتبه کاربر"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) + 1 as rank
            FROM users 
            WHERE score > (SELECT score FROM users WHERE user_id = ?)
            AND is_blocked = 0
        ''', (user_id,))
        result = cursor.fetchone()
        return result['rank'] if result else None

    # ============ متدهای پیام و حافظه ============

    def save_message(self, user_id, message_text, bot_response, 
                     message_type='text', intent=None, sentiment=None):
        """ذخیره پیام با جزئیات کامل"""
        cursor = self.conn.cursor()
        now = datetime.now()

        # ذخیره پیام
        cursor.execute('''
            INSERT INTO messages (
                user_id, message_text, bot_response, message_type,
                intent, sentiment, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, message_text, bot_response, message_type, intent, sentiment, now))

        # بروزرسانی آمار کاربر
        cursor.execute('''
            UPDATE users SET 
                total_messages = total_messages + 1,
                last_activity = ?
            WHERE user_id = ?
        ''', (now, user_id))

        self.conn.commit()

    def get_user_messages(self, user_id, limit=50):
        """دریافت تاریخچه پیام‌های کاربر"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT message_text, bot_response, message_type, intent, timestamp
            FROM messages 
            WHERE user_id = ? AND is_deleted = 0
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]

    def get_last_conversation(self, user_id, count=10):
        """دریافت آخرین گفتگوها"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT message_text, bot_response, timestamp
            FROM messages 
            WHERE user_id = ? AND is_deleted = 0
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (user_id, count))
        messages = cursor.fetchall()
        return [dict(row) for row in reversed(messages)]

    # ============ متدهای حافظه کاربر ============

    def save_user_memory(self, user_id, fact_key, fact_value):
        """ذخیره یک واقعیت در حافظه کاربر"""
        cursor = self.conn.cursor()
        now = datetime.now()

        # دریافت حافظه فعلی
        cursor.execute('SELECT remembered_facts FROM user_memory WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()

        if row:
            facts = json.loads(row['remembered_facts'])
        else:
            facts = {}
            cursor.execute('''
                INSERT INTO user_memory (user_id, remembered_facts, updated_at)
                VALUES (?, '{}', ?)
            ''', (user_id, now))

        # بروزرسانی واقعیت
        facts[fact_key] = fact_value

        cursor.execute('''
            UPDATE user_memory SET 
                remembered_facts = ?,
                updated_at = ?
            WHERE user_id = ?
        ''', (json.dumps(facts, ensure_ascii=False), now, user_id))

        self.conn.commit()

    def get_user_memory(self, user_id):
        """دریافت تمام حافظه کاربر"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM user_memory WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        if row:
            memory = dict(row)
            # تبدیل JSON به دیکشنری
            for key in ['remembered_facts', 'preferences', 'interaction_patterns',
                       'favorite_topics', 'personality_traits', 'interests',
                       'last_topics', 'custom_data']:
                if memory.get(key):
                    try:
                        memory[key] = json.loads(memory[key])
                    except:
                        pass
            return memory
        return None

    def remember_user_info(self, user_id, info_type, info_data):
        """به خاطر سپردن اطلاعات کاربر"""
        memory = self.get_user_memory(user_id) or {}
        remembered = memory.get('remembered_facts', {})

        if info_type == 'name':
            remembered['user_name'] = info_data
        elif info_type == 'age':
            remembered['age'] = info_data
        elif info_type == 'location':
            remembered['location'] = info_data
        elif info_type == 'job':
            remembered['job'] = info_data
        elif info_type == 'hobby':
            remembered['hobby'] = info_data
        elif info_type == 'favorite_anime':
            remembered['favorite_anime'] = info_data

        self.save_user_memory(user_id, 'remembered_facts', json.dumps(remembered, ensure_ascii=False))

    def update_user_preferences(self, user_id, preferences):
        """بروزرسانی تنظیمات کاربر"""
        cursor = self.conn.cursor()
        now = datetime.now()

        cursor.execute('SELECT user_id FROM user_memory WHERE user_id = ?', (user_id,))
        if cursor.fetchone():
            cursor.execute('''
                UPDATE user_memory SET 
                    preferences = ?,
                    updated_at = ?
                WHERE user_id = ?
            ''', (json.dumps(preferences, ensure_ascii=False), now, user_id))
        else:
            cursor.execute('''
                INSERT INTO user_memory (user_id, preferences, updated_at)
                VALUES (?, ?, ?)
            ''', (user_id, json.dumps(preferences, ensure_ascii=False), now))

        self.conn.commit()

    def add_user_interest(self, user_id, interest):
        """اضافه کردن علاقه‌مندی کاربر"""
        memory = self.get_user_memory(user_id) or {}
        interests = memory.get('interests', [])

        if isinstance(interests, str):
            try:
                interests = json.loads(interests)
            except:
                interests = []

        if interest not in interests:
            interests.append(interest)

        self.update_user_memory_field(user_id, 'interests', interests)

    def update_user_memory_field(self, user_id, field, value):
        """بروزرسانی یک فیلد خاص در حافظه"""
        cursor = self.conn.cursor()
        now = datetime.now()

        cursor.execute('SELECT user_id FROM user_memory WHERE user_id = ?', (user_id,))
        if cursor.fetchone():
            cursor.execute(f'''
                UPDATE user_memory SET 
                    {field} = ?,
                    updated_at = ?
                WHERE user_id = ?
            ''', (json.dumps(value, ensure_ascii=False), now, user_id))
        else:
            cursor.execute(f'''
                INSERT INTO user_memory (user_id, {field}, updated_at)
                VALUES (?, ?, ?)
            ''', (user_id, json.dumps(value, ensure_ascii=False), now))

        self.conn.commit()

    # ============ متدهای دستاوردها ============

    def add_achievement(self, user_id, achievement_key):
        """اضافه کردن دستاورد به کاربر"""
        from handlers.anime_handler import ACHIEVEMENTS

        achievement_data = ACHIEVEMENTS.get(achievement_key, {})
        if not achievement_data:
            return False

        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO achievements (
                    user_id, achievement_key, achievement_name, 
                    achievement_desc, icon
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                user_id, achievement_key,
                achievement_data.get('name', achievement_key),
                achievement_data.get('desc', ''),
                achievement_data.get('icon', '🏆')
            ))
            self.conn.commit()
            return cursor.rowcount > 0
        except:
            return False

    def get_user_achievements(self, user_id):
        """دریافت دستاوردهای کاربر"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM achievements 
            WHERE user_id = ? 
            ORDER BY earned_at DESC
        ''', (user_id,))
        return [dict(row) for row in cursor.fetchall()]

    # ============ متدهای جلسات ============

    def start_session(self, user_id, session_id):
        """شروع جلسه جدید"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO sessions (user_id, session_id, started_at)
            VALUES (?, ?, ?)
        ''', (user_id, session_id, datetime.now()))

        cursor.execute('''
            UPDATE users SET 
                session_count = session_count + 1,
                last_activity = ?
            WHERE user_id = ?
        ''', (datetime.now(), user_id))

        self.conn.commit()

    def end_session(self, session_id):
        """پایان جلسه"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE sessions SET 
                ended_at = ?,
                is_active = 0,
                duration = (
                    SELECT CAST((julianday(?) - julianday(started_at)) * 86400 AS INTEGER)
                    FROM sessions WHERE session_id = ?
                )
            WHERE session_id = ? AND is_active = 1
        ''', (datetime.now(), datetime.now(), session_id, session_id))
        self.conn.commit()

    # ============ متدهای فعالیت ============

    def log_activity(self, user_id, action, action_type='interaction', details=None):
        """ثبت فعالیت کاربر"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO activity_log (user_id, action, action_type, details, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, action, action_type, 
              json.dumps(details or {}, ensure_ascii=False), datetime.now()))
        self.conn.commit()

    # ============ متدهای آماری ============

    def get_users_count(self):
        """تعداد کل کاربران"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM users WHERE is_blocked = 0')
        return cursor.fetchone()['count']

    def get_total_points(self):
        """مجموع امتیازات"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT SUM(score) as total FROM users')
        result = cursor.fetchone()
        return result['total'] or 0

    def get_daily_stats(self, date=None):
        """آمار روزانه"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM daily_stats WHERE date = ?', (date,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_daily_stats(self):
        """بروزرسانی آمار امروز"""
        today = datetime.now().strftime('%Y-%m-%d')
        cursor = self.conn.cursor()

        # محاسبه آمار
        cursor.execute('SELECT COUNT(*) as count FROM users WHERE DATE(join_date) = ?', (today,))
        new_users = cursor.fetchone()['count']

        cursor.execute('SELECT COUNT(*) as count FROM users WHERE DATE(last_activity) = ?', (today,))
        active_users = cursor.fetchone()['count']

        cursor.execute('SELECT COUNT(*) as count FROM messages WHERE DATE(timestamp) = ?', (today,))
        total_messages = cursor.fetchone()['count']

        cursor.execute('''
            INSERT OR REPLACE INTO daily_stats (date, new_users, active_users, total_messages)
            VALUES (?, ?, ?, ?)
        ''', (today, new_users, active_users, total_messages))

        self.conn.commit()

    # ============ متدهای کاربران مسدود ============

    def block_user(self, user_id):
        """مسدود کردن کاربر"""
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET is_blocked = 1 WHERE user_id = ?', (user_id,))
        self.conn.commit()

    def unblock_user(self, user_id):
        """رفع مسدودیت کاربر"""
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET is_blocked = 0 WHERE user_id = ?', (user_id,))
        self.conn.commit()

    def get_blocked_users(self):
        """لیست کاربران مسدود"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE is_blocked = 1')
        return [dict(row) for row in cursor.fetchall()]

    # ============ متدهای نوتیفیکیشن ============

    def add_notification(self, user_id, title, message, notification_type='info', action_url=None):
        """اضافه کردن نوتیفیکیشن"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO notifications (user_id, title, message, notification_type, action_url)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, title, message, notification_type, action_url))
        self.conn.commit()

    def get_unread_notifications(self, user_id):
        """نوتیفیکیشن‌های خوانده نشده"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM notifications 
            WHERE user_id = ? AND is_read = 0 
            ORDER BY created_at DESC
        ''', (user_id,))
        return [dict(row) for row in cursor.fetchall()]

    # ============ پاکسازی و نگهداری ============

    def cleanup_old_data(self, days=90):
        """پاکسازی داده‌های قدیمی"""
        cursor = self.conn.cursor()
        cutoff = datetime.now().timestamp() - (days * 86400)
        cutoff_date = datetime.fromtimestamp(cutoff).strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('DELETE FROM activity_log WHERE timestamp < ?', (cutoff_date,))
        cursor.execute('DELETE FROM messages WHERE timestamp < ?', (cutoff_date,))

        self.conn.commit()


# ایجاد نمونه سراسری
db = Database()
