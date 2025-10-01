from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

with get_db_connection() as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise TEXT NOT NULL,
            reps INTEGER NOT NULL,
            sets INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()

@app.route('/')
def index():
    conn = get_db_connection()
    workouts = conn.execute('SELECT * FROM workouts ORDER BY date DESC').fetchall()
    totals = {}
    for workout in workouts:
        ex = workout['exercise']
        if ex not in totals:
            totals[ex] = {'reps': 0, 'sets': 0, 'volume': 0}
        totals[ex]['reps'] += workout['reps']
        totals[ex]['sets'] += workout['sets']
        totals[ex]['volume'] += workout['reps'] * workout['sets']
    conn.close()
    return render_template('index.html', workouts=workouts, totals=totals)

@app.route('/log', methods=['POST'])
def log_workout():
    exercise = request.form['exercise']
    reps = request.form['reps']
    sets = request.form['sets']
    if exercise and reps.isdigit() and sets.isdigit():
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = get_db_connection()
        conn.execute('INSERT INTO workouts (exercise, reps, sets, date) VALUES (?, ?, ?, ?)',
                     (exercise, int(reps), int(sets), date))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)