from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DB_PATH = '/root/mixart/data/mixart.db'

# Database yaratish
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER,
            quantity INTEGER DEFAULT 0
        )''')
        conn.commit()
        conn.close()
        print("✅ Database yaratildi")

init_db()

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mixart Admin - Ishlamoqda</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0; padding: 0; 
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                text-align: center;
                max-width: 600px;
            }
            h1 { color: #333; margin-bottom: 20px; }
            .status { 
                background: #4CAF50; 
                color: white; 
                padding: 10px 20px;
                border-radius: 50px;
                display: inline-block;
                margin: 20px 0;
            }
            .info { 
                background: #f5f5f5; 
                padding: 20px; 
                border-radius: 10px;
                margin: 20px 0;
                text-align: left;
            }
            .btn {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 12px 30px;
                border-radius: 5px;
                text-decoration: none;
                margin: 10px;
                font-weight: bold;
            }
            .btn:hover { background: #5a67d8; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏪 Mixart Admin Panel</h1>
            <div class="status">✅ ISHLAYAPTI</div>
            
            <div class="info">
                <p><strong>🌐 URL:</strong> http://46.101.172.299:5000</p>
                <p><strong>🤖 Bot:</strong> @mixart_shop_bot</p>
                <p><strong>📅 Sana:</strong> ''' + os.popen('date').read().strip() + '''</p>
                <p><strong>💾 Database:</strong> ''' + ("✅ Mavjud" if os.path.exists(DB_PATH) else "❌ Yo'q") + '''</p>
            </div>
            
            <div style="margin-top: 30px;">
                <a href="/products" class="btn">📦 Mahsulotlar</a>
                <a href="/orders" class="btn">🛒 Buyurtmalar</a>
                <a href="/stats" class="btn">📊 Statistika</a>
            </div>
            
            <div style="margin-top: 30px; color: #666; font-size: 14px;">
                <p>Server: Ubuntu 24.04 | Python 3 | Flask</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/products')
def products():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name, price, quantity FROM products')
    products = c.fetchall()
    conn.close()
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mahsulotlar</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #f2f2f2; }
            .btn { padding: 8px 16px; margin: 5px; border: none; border-radius: 4px; cursor: pointer; }
            .btn-add { background: #4CAF50; color: white; }
            .btn-back { background: #666; color: white; }
        </style>
    </head>
    <body>
        <h1>📦 Mahsulotlar</h1>
        <button class="btn btn-add" onclick="addProduct()">➕ Yangi mahsulot</button>
        <button class="btn btn-back" onclick="window.location='/'">🏠 Bosh sahifa</button>
        
        <table>
            <tr><th>ID</th><th>Nomi</th><th>Narxi</th><th>Miqdori</th><th>Harakat</th></tr>
    '''
    
    for p in products:
        html += f'<tr><td>{p[0]}</td><td>{p[1]}</td><td>{p[2]:,} so\'m</td><td>{p[3]}</td><td><button onclick="deleteProduct({p[0]})">🗑️</button></td></tr>'
    
    html += '''
        </table>
        
        <script>
        function addProduct() {
            const name = prompt('Mahsulot nomi:');
            if(!name) return;
            const price = prompt('Narxi (so\'m):');
            const quantity = prompt('Miqdori:');
            
            fetch('/api/products', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name, price, quantity})
            })
            .then(() => location.reload());
        }
        
        function deleteProduct(id) {
            if(confirm('O\'chirishni tasdiqlaysizmi?')) {
                fetch('/api/products/' + id, {method: 'DELETE'})
                .then(() => location.reload());
            }
        }
        </script>
    </body>
    </html>
    '''
    return html

# API endpoints
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)',
             (data['name'], data['price'], data['quantity']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/stats')
def stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM products')
    product_count = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM orders')
    order_count = c.fetchone()[0] if os.path.exists(DB_PATH) else 0
    
    conn.close()
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>Statistika</title></head>
    <body>
        <h1>📊 Statistika</h1>
        <p>📦 Mahsulotlar: {product_count}</p>
        <p>🛒 Buyurtmalar: {order_count}</p>
        <button onclick="window.location='/'">🏠 Bosh sahifa</button>
    </body>
    </html>
    '''

@app.route('/orders')
def orders():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Buyurtmalar</title></head>
    <body>
        <h1>🛒 Buyurtmalar</h1>
        <p>Tez orada...</p>
        <button onclick="window.location='/'">🏠 Bosh sahifa</button>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("🚀 Mixart Admin Panel ishga tushmoqda...")
    print("🌐 http://46.101.172.299:5000")
    print("📱 Bot bilan integratsiya")
    
    # Portni tekshirish
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 5000))
    
    if result == 0:
        print("⚠️  Port 5000 band! 5050-portda ishga tushiraman...")
        app.run(host='0.0.0.0', port=5050, debug=True)
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)
