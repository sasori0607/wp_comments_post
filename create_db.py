import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''CREATE TABLE IF NOT EXISTS comments
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              post_id INTEGER,
              author_name TEXT,
              author_email TEXT,
              content TEXT)''')

conn.close()
