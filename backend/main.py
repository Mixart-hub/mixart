from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import sqlite3

app = FastAPI()

# ===== ADMIN LOGIN =====
ADMIN_LOGIN = "Malika"
ADMIN_PASSWORD = "Mixart1997"

# ===== SESSION =====
app.add_middleware(
    SessionMiddleware,
    secret_key="mixart-secret-key"
)

# ===== DATABASE =====
def db():
    return sqlite3.connect("mixart.db")


# ===== LOGIN PAGE =====
@app.get("/", response_class=HTMLResponse)
def login_page():
    return """
    <h2>MIXART ADMIN</h2>
    <form method="post">
      <input name="login" placeholder="Login"><br><br>
      <input type="password" name="password" placeholder="Parol"><br><br>
      <button>Kirish</button>
    </form>
    """


# ===== LOGIN POST =====
@app.post("/", response_class=HTMLResponse)
def login_post(
    request: Request,
    login: str = Form(...),
    password: str = Form(...)
):
    if login != ADMIN_LOGIN or password != ADMIN_PASSWORD:
        return """
        <h3 style="color:red">❌ Login yoki parol xato</h3>
        <a href="/">🔙 Orqaga</a>
        """

    request.session["admin"] = True
    return RedirectResponse("/dashboard", status_code=302)


# ===== DASHBOARD =====
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if not request.session.get("admin"):
        return RedirectResponse("/", status_code=302)

    con = db()
    cur = con.cursor()

    users = cur.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    orders = cur.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    income = cur.execute(
        "SELECT IFNULL(SUM(amount),0) FROM orders WHERE status='tasdiqlandi'"
    ).fetchone()[0]

    return f"""
    <h2>📊 Admin panel</h2>

    <ul>
      <li>👤 Users: <b>{users}</b></li>
      <li>📦 Orders: <b>{orders}</b></li>
      <li>💰 Income: <b>{income}</b> so'm</li>
    </ul>

    <a href="/orders">📦 Buyurtmalar</a><br><br>
    <a href="/logout">🚪 Chiqish</a>
    """


# ===== ORDERS =====
@app.get("/orders", response_class=HTMLResponse)
def orders_page(request: Request):
    if not request.session.get("admin"):
        return RedirectResponse("/", status_code=302)

    con = db()
    cur = con.cursor()

    rows = cur.execute("""
        SELECT orders.id, users.username, orders.amount, orders.status
        FROM orders
        LEFT JOIN users ON users.id = orders.user_id
        ORDER BY orders.id DESC
    """).fetchall()

    html = "<h2>📦 Buyurtmalar</h2><table border=1 cellpadding=5>"
    html += "<tr><th>ID</th><th>User</th><th>Summa</th><th>Status</th></tr>"

    for r in rows:
        html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"

    html += "</table><br><a href='/dashboard'>⬅️ Orqaga</a>"
    return html


# ===== LOGOUT =====
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)
