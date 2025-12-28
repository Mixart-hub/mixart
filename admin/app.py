from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = "/root/mixart/data/mixart.db"


@app.route("/")
def dashboard():
    return """
    <h2>Mixart Analytics</h2>
    <canvas id="line"></canvas>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    fetch('/api/daily')
      .then(r => r.json())
      .then(data => {
        new Chart(document.getElementById('line'), {
          type: 'line',
          data: {
            labels: data.map(x => x[0]),
            datasets: [{
              label: 'Kunlik savdo',
              data: data.map(x => x[1]),
              borderWidth: 3
            }]
          }
        })
      })
    </script>
    """
    

@app.route("/api/daily")
def daily():
    db = sqlite3.connect(DB_PATH)
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
    return jsonify(rows)
