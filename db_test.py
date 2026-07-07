import sqlite3

# Connect to a database file (creates it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
               CREATE TABLE IF NOT EXISTS users (
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    username TEXT NOT NULL,
                                                    email TEXT NOT NULL
               )
               ''')

# Insert a row
cursor.execute('INSERT INTO users (username, email) VALUES (?, ?)', ('daniel', 'daniel@example.com'))
conn.commit()

# Read it back
cursor.execute('SELECT * FROM users')
print(cursor.fetchall())

conn.close()