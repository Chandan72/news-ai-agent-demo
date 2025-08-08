# test_sqlite.py
import sqlite3
print("✅ sqlite3 is available!")
print(f"SQLite version: {sqlite3.sqlite_version}")

# Test creating a database
conn = sqlite3.connect(':memory:')  # In-memory database for testing
cursor = conn.cursor()
cursor.execute('CREATE TABLE test (id INTEGER, name TEXT)')
cursor.execute('INSERT INTO test VALUES (1, "Hello World")')
cursor.execute('SELECT * FROM test')
result = cursor.fetchone()
print(f"Test query result: {result}")
conn.close()
print("✅ sqlite3 is working perfectly!")
