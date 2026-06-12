from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('notes.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_note', methods=['POST'])
def add_note():
    
    data = request.get_json()
    note = data['content']

    conn = sqlite3.connect('notes.db')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO notes(content) VALUES(?)",
        (note,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Note Saved Successfully"
    })
@app.route('/notes')
def get_notes():

    conn = sqlite3.connect('notes.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM notes")
    rows = cur.fetchall()

    conn.close()

    notes = []

    for row in rows:
        notes.append({
            "id": row[0],
            "content": row[1]
        })

    return jsonify(notes)

if __name__ == '__main__':
    app.run(debug=True)