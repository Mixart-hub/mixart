#!/bin/bash
echo "📊 MIXART TIZIM HOLATI"
echo "======================"
echo ""

# Protsesslarni tekshirish
echo "🖥️  PROTSESSLAR:"
if pgrep -f "python3 admin/app.py" > /dev/null; then
    echo "   ✅ Admin panel ishlayapti"
else
    echo "   ❌ Admin panel ishlamayapti"
fi

if pgrep -f "python3 bot/main.py" > /dev/null; then
    echo "   ✅ Telegram bot ishlayapti"
else
    echo "   ❌ Telegram bot ishlamayapti"
fi

# Portlarni tekshirish
echo ""
echo "🌐 PORTLAR:"
if netstat -tlnp 2>/dev/null | grep :5000 > /dev/null; then
    echo "   ✅ Port 5000 (admin) ochiq"
else
    echo "   ❌ Port 5000 yopiq"
fi

# Database holati
echo ""
echo "🗄️  DATABASE:"
DB_FILE="data/mixart.db"
if [ -f "$DB_FILE" ]; then
    SIZE=$(du -h "$DB_FILE" | cut -f1)
    ROWS=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM orders;" 2>/dev/null || echo "0")
    echo "   ✅ Database mavjud ($SIZE)"
    echo "   📊 Buyurtmalar soni: $ROWS"
else
    echo "   ❌ Database topilmadi"
fi

# Log fayllari
echo ""
echo "📋 LOG FAYLLARI:"
if [ -f "bot.log" ]; then
    BOT_SIZE=$(du -h bot.log | cut -f1)
    echo "   🤖 Bot logi: $BOT_SIZE"
else
    echo "   🤖 Bot logi: yo'q"
fi

if [ -f "admin.log" ]; then
    ADMIN_SIZE=$(du -h admin.log | cut -f1)
    echo "   🌐 Admin logi: $ADMIN_SIZE"
else
    echo "   🌐 Admin logi: yo'q"
fi

# So'nggi xatolar
echo ""
echo "⚠️  SO'NGGI XATOLAR (agar bo'lsa):"
echo "----------------------------------"
grep -i "error\|exception\|fail" bot.log | tail -3
echo ""
