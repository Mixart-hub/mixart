#!/bin/bash
echo "🛑 Mixart tizimi to'xtatilmoqda..."
echo ""

# Protsesslarni to'xtatish
pkill -f "python3 admin/app.py" 2>/dev/null && echo "✅ Admin panel to'xtatildi"
pkill -f "python3 bot/main.py" 2>/dev/null && echo "✅ Telegram bot to'xtatildi"

sleep 2

echo ""
echo "🎯 Tizim to'liq to'xtatildi!"
echo "🔁 Qayta ishga tushirish uchun: ./start.sh"
