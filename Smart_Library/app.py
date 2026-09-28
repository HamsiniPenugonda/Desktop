from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = "library.db"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            copies INTEGER NOT NULL
        )
    """)

    count = connection.execute(
        "SELECT COUNT(*) FROM books"
    ).fetchone()[0]

    if count == 0:
        books = [
            ("Python Crash Course", "Eric Matthes", "Programming", 3),
            ("Learning Python", "Mark Lutz", "Programming", 0),
            ("Clean Code", "Robert C. Martin", "Programming", 2),
            ("Atomic Habits", "James Clear", "Self Help", 1),
            ("The Alchemist", "Paulo Coelho", "Fiction", 4),
            ("Data Science from Scratch", "Joel Grus", "Data Science", 0),
            ("Java: The Complete Reference", "Herbert Schildt", "Programming", 2),
            ("Computer Networks", "Andrew S. Tanenbaum", "Networking", 1)
        ]

        connection.executemany("""
            INSERT INTO books
            (title, author, category, copies)
            VALUES (?, ?, ?, ?)
        """, books)

    connection.commit()
    connection.close()


@app.route("/")
def home():

    search = request.args.get("search", "").strip()

    connection = get_db()

    if search:
        books = connection.execute("""
            SELECT * FROM books
            WHERE title LIKE ?
               OR author LIKE ?
               OR category LIKE ?
            ORDER BY title
        """, (
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        )).fetchall()

    else:
        books = connection.execute("""
            SELECT * FROM books
            ORDER BY title
        """).fetchall()

    connection.close()

    return render_template(
        "index.html",
        books=books,
        search=search
    )


if __name__ == "__main__":
    initialize_database()

    app.run(debug=True)