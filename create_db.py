import sqlite3

# connection = sqlite3.connect('db/categories.db')
connection = sqlite3.connect('db/Home_Colour.db')
cursor = connection.cursor()

# sql = """Create table categories (id INTEGER PRIMARY KEY AUTOINCREMENT, category_name varchar(100),
# total_amount INTEGER, last_modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)"""
# cursor.execute(sql)
# connection.commit()
result = cursor.execute("Select * from Home_Colour")
articles = cursor.fetchall()
print(articles)

