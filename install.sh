#!/bin/bash
set -e

echo "🔥 Mixart full install boshlandi..."

# SYSTEM
apt update
apt install -y python3 python3-venv python3-pip nginx

# PROJECT
cd /root/mixart

# VENV
python3 -m venv venv
source venv/bin/activate

# PYTHON DEPS
pip install --upgrade pip
pip install gunicorn flask

# SIMPLE APP (agar yo‘q bo‘lsa)
cat > admin_app.py <<'EOF'
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Mixart Backend OK 🚀"

if __name__ == "__main__":
    app.run()
EOF

# SYSTEMD SERVICE
cat > /etc/systemd/system/mixart.service <<'EOF'
[Unit]
Description=Mixart Backend (Gunicorn)
After=network.target

[Service]
User=root
WorkingDirectory=/root/mixart
ExecStart=/root/mixart/venv/bin/gunicorn -w 2 -b 127.0.0.1:8000 admin_app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# SYSTEMD ENABLE
systemctl daemon-reload
systemctl enable mixart
systemctl start mixart

# NGINX
cat > /etc/nginx/sites-available/mixart <<'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/mixart /etc/nginx/sites-enabled/mixart

nginx -t
systemctl restart nginx

echo "✅ Mixart o‘rnatildi!"
echo

