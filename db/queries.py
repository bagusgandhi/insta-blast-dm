import sqlite3
from .database import get_db_connection

def insert_profile(profile_link):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
        INSERT INTO profiles (profile_link) VALUES (?)
        ''', (profile_link,))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Profile {profile_link} already exists.")
    finally:
        conn.close()

def mark_as_delivered(profile_link):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE profiles SET delivered = 1 WHERE profile_link = ?
    ''', (profile_link,))
    conn.commit()
    conn.close()

def has_been_delivered(profile_link):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT delivered FROM profiles WHERE profile_link = ?
    ''', (profile_link,))
    result = cursor.fetchone()
    conn.close()

    if result and result['delivered']:
        return True
    return False