import sqlite3

# Create database connection
connection = sqlite3.connect("finance.db")

# Create cursor
cursor = connection.cursor()

# Create Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

# Create Income Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    amount REAL,
    source TEXT
)
""")


# Create Expense Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    amount REAL,
    category TEXT
)
""")


# Read Existing User
cursor.execute(
    "SELECT * FROM users WHERE email=?",
    ("rajj@gmail.com",)
)

user = cursor.fetchone()

print(user)

connection.commit()
connection.close()

print("✅ Database Ready Successfully")