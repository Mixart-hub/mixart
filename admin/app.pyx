from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

# ---------- DAILY STATS API ----------
@app.route("/api/daily")
def daily():
    db = sqlite3.connect("/root/mixart/data/mixart.db")
    c = db.cursor()

    c.execute("""
        SELECT date(created_at), SUM(total)
        FROM orders
        GROUP BY date(created_at)
        ORDER BY date(created_at) DESC
        LIMIT 7
    """)

    rows = c.fetchall()
    db.close()
    return jsonify(rows[::-1])

# ---------- DASHBOARD ----------
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
