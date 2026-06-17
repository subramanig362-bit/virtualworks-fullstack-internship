from flask import Flask, render_template, redirect
import sqlite3
import requests
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("quotes.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS quotes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote TEXT,
        author TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

@app.route('/')
def home():

    conn = sqlite3.connect("quotes.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT quote, author, created_at
    FROM quotes
    ORDER BY id DESC
    """)

    history = cur.fetchall()

    conn.close()

    return render_template(
        "index.html",
        history=history
    )

@app.route('/generate')
def generate():

    response = requests.get(
    "https://zenquotes.io/api/random"
    )

    data = response.json()

    quote = data[0]["q"]
    author = data[0]["a"]

    created_at = datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )

    conn = sqlite3.connect("quotes.db")
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO quotes
        (quote, author, created_at)
        VALUES (?,?,?)
        """,
        (quote, author, created_at)
    )

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)