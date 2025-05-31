import sqlite3

conn = sqlite3.connect("transfers.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS transfer_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT NOT NULL
)
''')

cursor.executemany('''
INSERT INTO transfer_requests (recipient, amount, currency)
VALUES (?, ?, ?)
''', [
    ('Alice', 100, 'USD')
#   ('Bob', 250, 'EUR'),
#    ('Charlie', 500, 'GBP')
])

conn.commit()
conn.close()

print("Database created with sample data.")