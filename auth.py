import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

DEFAULT_AVATAR = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_auth_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'UI/UX Designer & Real Estate Investor',
            avatar TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_valuations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            location TEXT NOT NULL,
            sqft REAL NOT NULL,
            bhk INTEGER NOT NULL,
            bath INTEGER NOT NULL,
            price_inr TEXT NOT NULL,
            price_usd TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Migration check for columns
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'role' not in columns:
        try: cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'UI/UX Designer'")
        except Exception: pass
    if 'avatar' not in columns:
        try: cursor.execute("ALTER TABLE users ADD COLUMN avatar TEXT")
        except Exception: pass

    # Create default demo user if not exists
    cursor.execute('SELECT * FROM users WHERE email = ?', ('demo@bengaluru.com',))
    if not cursor.fetchone():
        demo_password = hash_password('password123')
        cursor.execute(
            'INSERT INTO users (name, email, password_hash, role, avatar) VALUES (?, ?, ?, ?, ?)',
            ('Ashok sp', 'demo@bengaluru.com', demo_password, 'UI/UX Designer & Real Estate Investor', DEFAULT_AVATAR)
        )
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register_user(name, email, password):
    email = email.strip().lower()
    name = name.strip()
    if not name or not email or not password:
        return False, "All fields are required."
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            return False, "User with this email already exists."
        
        pwd_hash = hash_password(password)
        cursor.execute('INSERT INTO users (name, email, password_hash, role, avatar) VALUES (?, ?, ?, ?, ?)',
                       (name, email, pwd_hash, 'Real Estate Investor', DEFAULT_AVATAR))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, {"id": user_id, "name": name, "email": email, "role": 'Real Estate Investor', "avatar": DEFAULT_AVATAR}
    except Exception as e:
        conn.close()
        return False, str(e)

def login_user(email, password):
    email = email.strip().lower()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and user['password_hash'] == hash_password(password):
        user_role = user['role'] if 'role' in user.keys() and user['role'] else 'Real Estate Investor'
        user_avatar = user['avatar'] if 'avatar' in user.keys() and user['avatar'] else DEFAULT_AVATAR
        return True, {"id": user['id'], "name": user['name'], "email": user['email'], "role": user_role, "avatar": user_avatar}
    return False, "Invalid email or password."

def update_user_profile(user_id, name, email, role=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if role:
            cursor.execute('UPDATE users SET name = ?, email = ?, role = ? WHERE id = ?',
                           (name, email, role, user_id))
        else:
            cursor.execute('UPDATE users SET name = ?, email = ? WHERE id = ?',
                           (name, email, user_id))
        conn.commit()
        conn.close()
        return True, "Profile updated successfully."
    except Exception as e:
        conn.close()
        return False, str(e)

def update_user_avatar(user_id, avatar_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET avatar = ? WHERE id = ?', (avatar_data, user_id))
        conn.commit()
        conn.close()
        return True, "Avatar updated successfully."
    except Exception as e:
        conn.close()
        return False, str(e)

def save_valuation(user_id, location, sqft, bhk, bath, price_inr, price_usd):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO saved_valuations (user_id, location, sqft, bhk, bath, price_inr, price_usd)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, location, sqft, bhk, bath, price_inr, price_usd))
        conn.commit()
        val_id = cursor.lastrowid
        conn.close()
        return True, val_id
    except Exception as e:
        conn.close()
        return False, str(e)

def get_saved_valuations(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM saved_valuations WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_saved_valuation(valuation_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM saved_valuations WHERE id = ? AND user_id = ?', (valuation_id, user_id))
    conn.commit()
    conn.close()
    return True
