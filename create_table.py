import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

### Users
# INTEGER --> Auto increment
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

### Items
create_item_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_item_table)

# cursor.execute("INSERT INTO items VALUES ('test', 10.99)")

conn.commit()
conn.close()