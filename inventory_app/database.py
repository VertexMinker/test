import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / 'app.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS items ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT, '
        'name TEXT, '
        'quantity INTEGER'
        ')'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS history ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT, '
        'item_id INTEGER, '
        'date TEXT, '
        'sold INTEGER'
        ')'
    )
    cur.execute('SELECT COUNT(*) FROM items')
    if cur.fetchone()[0] == 0:
        sample_items = [
            ('Bluetooth Speaker', 10),
            ('Wireless Earbuds', 25),
            ('USB-C Cable', 50)
        ]
        cur.executemany('INSERT INTO items (name, quantity) VALUES (?, ?)', sample_items)
    conn.commit()
    return conn

def get_connection():
    return sqlite3.connect(DB_PATH)
