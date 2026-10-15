import os
import sqlite3
from datetime import date, timedelta


DATABASE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "sharehub.db"
)


def connect():

    return sqlite3.connect(DATABASE)


def create_table():

    connection = connect()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            owner TEXT NOT NULL,
            status TEXT NOT NULL,
            borrower TEXT,
            due_date TEXT DEFAULT ''
        )
    """)

    # upgrade older databases that do not have the due_date column yet
    cursor.execute("PRAGMA table_info(items)")

    columns = [column[1] for column in cursor.fetchall()]

    if "due_date" not in columns:
        cursor.execute(
            "ALTER TABLE items ADD COLUMN due_date TEXT DEFAULT ''"
        )

    connection.commit()

    connection.close()


def add_item(
    name,
    category,
    description,
    owner
):

    connection = connect()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO items
        (name, category, description, owner, status, borrower)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        category,
        description,
        owner,
        "Available",
        ""
    ))

    item_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return item_id


def get_all_items():

    connection = connect()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            category,
            description,
            owner,
            status,
            borrower,
            due_date
        FROM items
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_item(item_id):

    connection = connect()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            category,
            description,
            owner,
            status,
            borrower,
            due_date
        FROM items
        WHERE id = ?
    """, (item_id,))

    item = cursor.fetchone()

    connection.close()

    return item


def update_item(item_id, name, category, description, owner):

    connection = connect()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE items
        SET name = ?, category = ?, description = ?, owner = ?
        WHERE id = ?
    """, (name, category, description, owner, item_id))

    changed = cursor.rowcount

    connection.commit()

    connection.close()

    return changed


def delete_item(item_id):

    connection = connect()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM items WHERE id = ?",
        (item_id,)
    )

    changed = cursor.rowcount

    connection.commit()

    connection.close()

    return changed


def borrow_item(item_id, borrower, days):

    due_date = (
        date.today() + timedelta(days=days)
    ).isoformat()

    connection = connect()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE items
        SET status = ?, borrower = ?, due_date = ?
        WHERE id = ? AND status = ?
    """, (
        "Borrowed",
        borrower,
        due_date,
        item_id,
        "Available"
    ))

    changed = cursor.rowcount

    connection.commit()

    connection.close()

    return changed


def return_item(item_id):

    connection = connect()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE items
        SET status = ?, borrower = ?, due_date = ?
        WHERE id = ? AND status = ?
    """, (
        "Available",
        "",
        "",
        item_id,
        "Borrowed"
    ))

    changed = cursor.rowcount

    connection.commit()

    connection.close()

    return changed


def get_statistics():

    connection = connect()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM items"
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM items WHERE status = 'Available'"
    )

    available = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM items WHERE status = 'Borrowed'"
    )

    borrowed = cursor.fetchone()[0]

    connection.close()

    return total, available, borrowed


def get_overdue_count():

    connection = connect()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM items
        WHERE status = 'Borrowed'
        AND due_date != ''
        AND due_date < ?
    """, (date.today().isoformat(),))

    overdue = cursor.fetchone()[0]

    connection.close()

    return overdue


def days_left(due_date):
    """Days until the due date (negative = days overdue), or None."""

    if not due_date:
        return None

    try:
        return (date.fromisoformat(due_date) - date.today()).days
    except ValueError:
        return None


create_table()