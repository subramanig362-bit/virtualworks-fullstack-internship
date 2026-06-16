from flask import Flask, render_template, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("coffee.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS coffees(
        id INTEGER PRIMARY KEY,
        name TEXT,
        votes INTEGER
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
            "INSERT INTO coffees(name,votes) VALUES (?,?)",
            coffees
        )

    conn.commit()
    conn.close()

def get_coffees():
    conn = sqlite3.connect("coffee.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM coffees")
    coffees = cur.fetchall()

    conn.close()
    return coffees

@app.route('/')
def home():
    coffees = get_coffees()
    return render_template("index.html", coffees=coffees)

@app.route('/vote/<int:id>')
def vote(id):

    conn = sqlite3.connect("coffee.db")
    cur = conn.cursor()

    cur.execute(
        "UPDATE coffees SET votes = votes + 1 WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)