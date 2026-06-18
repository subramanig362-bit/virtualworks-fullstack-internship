from flask import Flask, render_template, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("team.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS team(
        id INTEGER PRIMARY KEY,
        name TEXT,
        role TEXT,
        status TEXT
    )
    """)

    cur.execute("SELECT COUNT(*) FROM team")

    if cur.fetchone()[0] == 0:
        members = [
            ("Alex Rivers","Senior Developer","Available"),
            ("Samantha Chen","UX Designer","Busy"),
            ("Jordan Taylor","Project Manager","Available"),
            ("Maria Garcia","Marketing Lead","Busy")
        ]

        cur.executemany(
            "INSERT INTO team(name,role,status) VALUES(?,?,?)",
            members
        )

    conn.commit()
    conn.close()

@app.route('/')
def home():

    conn = sqlite3.connect("team.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM team")
    members = cur.fetchall()

    available = sum(1 for m in members if m[3] == "Available")
    busy = len(members) - available

    conn.close()

    return render_template(
        "index.html",
        members=members,
        available=available,
        busy=busy
    )

@app.route('/toggle/<int:id>')
def toggle(id):

    conn = sqlite3.connect("team.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT status FROM team WHERE id=?",
        (id,)
    )

    status = cur.fetchone()[0]

    new_status = "Busy" if status == "Available" else "Available"

    cur.execute(
        "UPDATE team SET status=? WHERE id=?",
        (new_status,id)
    )

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)