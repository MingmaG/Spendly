import os
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "expense_tracker.db")
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    db.commit()
    db.close()


def get_user_by_email(email):
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    db.close()
    return row


def get_user_by_id(user_id):
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    db.close()
    return row


def create_user(name, email, password_hash):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    db.commit()
    user_id = cursor.lastrowid
    db.close()
    return user_id


def seed_db():
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count > 0:
        db.close()
        return

    password_hash = generate_password_hash("demo123")
    cursor = db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )
    user_id = cursor.lastrowid

    month_start = datetime.now().replace(day=1)

    expenses = [
        (45.50, "Food", 1, "Grocery shopping"),
        (12.00, "Transport", 3, "Bus pass top-up"),
        (89.99, "Bills", 5, "Electricity bill"),
        (25.00, "Health", 7, "Pharmacy"),
        (60.00, "Entertainment", 10, "Movie night"),
        (150.00, "Shopping", 13, "New shoes"),
        (30.00, "Other", 15, "Miscellaneous"),
        (18.75, "Food", 18, "Coffee with friends"),
    ]

    for amount, category, day_offset, description in expenses:
        date = month_start.replace(day=min(day_offset, 28)).strftime("%Y-%m-%d")
        db.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, amount, category, date, description),
        )

    db.commit()
    db.close()
