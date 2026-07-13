import sqlite3

DB_NAME = "expenses.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    """Creates the transactions table if it doesn't already exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            date TEXT NOT NULL,
            note TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_transaction(t_type, amount, category, date, note):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (type, amount, category, date, note)
        VALUES (?, ?, ?, ?, ?)
    """, (t_type, amount, category, date, note))
    conn.commit()
    conn.close()


def get_all_transactions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, type, amount, category, date, note FROM transactions ORDER BY date")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_monthly_report(year_month):
    """year_month should be in 'YYYY-MM' format, e.g. '2026-07'."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT type, SUM(amount) FROM transactions
        WHERE date LIKE ?
        GROUP BY type
    """, (year_month + "%",))
    totals_by_type = cursor.fetchall()

    cursor.execute("""
        SELECT category, SUM(amount) FROM transactions
        WHERE date LIKE ? AND type = 'expense'
        GROUP BY category
    """, (year_month + "%",))
    totals_by_category = cursor.fetchall()

    conn.close()
    return totals_by_type, totals_by_category


def search_transactions(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    like_pattern = f"%{keyword}%"
    cursor.execute("""
        SELECT id, type, amount, category, date, note FROM transactions
        WHERE category LIKE ? OR note LIKE ? OR date LIKE ?
        ORDER BY date
    """, (like_pattern, like_pattern, like_pattern))
    rows = cursor.fetchall()
    conn.close()
    return rows