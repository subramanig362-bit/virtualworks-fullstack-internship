from flask import Flask, render_template, redirect, abort
import sqlite3
from contextlib import contextmanager

app = Flask(__name__)

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect("coffee.db")
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS coffees(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            votes INTEGER DEFAULT 0
        )
        """)
        
        cur.execute("SELECT COUNT(*) FROM coffees")
        if cur.fetchone()[0] == 0:
            coffees = [
                ("Espresso", 5),
                ("Cappuccino", 3),
                ("Cold Brew", 4),
                ("Vanilla Latte", 6),
                ("Mocha Chino", 2),
                ("Irish Coffee", 1),
                ("Americano", 7)
            ]
            cur.executemany(
                "INSERT INTO coffees(name, votes) VALUES (?, ?)",
                coffees
            )
        conn.commit()

def get_coffees():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM coffees ORDER BY votes DESC")
        return cur.fetchall()

@app.route('/')
def home():
    try:
        coffees = get_coffees()
        return render_template("index.html", coffees=coffees)
    except sqlite3.Error as e:
        abort(500)

@app.route('/vote/<int:coffee_id>')
def vote(coffee_id):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            # Verify coffee exists first
            cur.execute("SELECT id FROM coffees WHERE id = ?", (coffee_id,))
            if not cur.fetchone():
                abort(404)
            
            cur.execute(
                "UPDATE coffees SET votes = votes + 1 WHERE id = ?",
                (coffee_id,)
            )
            conn.commit()
    except sqlite3.Error:
        abort(500)
    
    return redirect('/')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)