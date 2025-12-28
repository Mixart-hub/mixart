#!/bin/bash

cd /root/mixart
source venv/bin/activate

# Hozirgi protsesslarni to'xtatish
pkill -f "python" 2>/dev/null
sleep 2

echo ""
echo "========================================"
echo "     MIXART ADMIN PANEL - FIXED        "
echo "========================================"
echo ""

# 1. Database ni tekshirish
if [ ! -f "data/mixart.db" ]; then
    echo "🗄️  Database yaratilmoqda..."
    sqlite3 data/mixart.db "VACUUM;"
fi

# 2. Admin panelni ishga tushirish
echo "🌐 Admin panel ishga tushmoqda..."
nohup python3 admin/simple_admin.py > admin.log 2>&1 &
sleep 3

# 3. Botni ishga tushirish
echo "🤖 Telegram bot ishga tushmoqda..."
nohup python3 bot/main.py > bot.log 2>&1 &
sleep 2

# 4. Natijalar
echo ""
echo "✅ TIZIM ISHGA TUSHIRILDI!"
echo ""
echo "📌 ADMIN PANEL (YANGI):"
echo "   🌐 http://46.101.172.299:5000"
echo "   🌐 http://46.101.172.299:5050 (agar 5000 band bo'lsa)"
echo ""
echo "📌 TELEGRAM BOT:"
echo "   🤖 @mixart_shop_bot"
echo ""
echo "📌 TEKSHIRISH:"
echo "   curl http://localhost:5000"
echo "   tail -f admin.log"
echo ""
echo "========================================"
