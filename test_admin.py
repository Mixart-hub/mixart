from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Test Admin</title></head>
    <body>
        <h1>✅ Mixart Test Admin</h1>
        <p>Server ishlayapti!</p>
        <p>IP: 46.101.172.299</p>
        <p>Port: 9000</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("🚀 Test server ishga tushmoqda...")
    print("🌐 http://46.101.172.299:9000")
    app.run(host='0.0.0.0', port=9000, debug=True)
