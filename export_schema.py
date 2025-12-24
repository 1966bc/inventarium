import sqlite3

conn = sqlite3.connect('sql/inventarium.db')
with open('schema.sql', 'w') as f:
    for row in conn.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL"):
        f.write(row[0] + ';\n\n')
conn.close()
print("Schema esportato in schema.sql")
