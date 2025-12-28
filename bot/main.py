#!/usr/bin/env python3
import logging
import sqlite3
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = '/root/mixart/data/mixart.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER,
        quantity INTEGER DEFAULT 0,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
        telegram_id INTEGER PRIMARY KEY,
        username TEXT,
        full_name TEXT,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        products TEXT,
        total INTEGER,
        status TEXT DEFAULT 'pending',
        payment_method TEXT DEFAULT 'naqd',
        phone TEXT,
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()

class MixartBot:
    def __init__(self, token):
        self.token = token
        self.application = Application.builder().token(token).build()
        init_db()
        self.setup_handlers()
    
    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("menu", self.menu_command))
        self.application.add_handler(CommandHandler("products", self.products_command))
        self.application.add_handler(CommandHandler("categories", self.categories_command))
        self.application.add_handler(CommandHandler("cart", self.cart_command))
        self.application.add_handler(CommandHandler("myorders", self.myorders_command))
        self.application.add_handler(CallbackQueryHandler(self.callback_handler))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO customers (telegram_id, username, full_name) VALUES (?, ?, ?)',
                 (user.id, user.username, user.full_name))
        conn.commit()
        conn.close()
        
        text = f"""👋 Salom {user.first_name}!

🏪 *Mixart Do'kon Botiga xush kelibsiz!*

📱 *Buyruqlar:*
/products - 📦 Mahsulotlar
/categories - 🗂️ Kategoriyalar
/cart - 🛒 Savatcha
/myorders - 📋 Buyurtmalarim
/menu - 🏠 Asosiy menyu

📍 *Aloqa:* +998 90 123 45 67
🕐 *Ish vaqti:* 9:00-18:00
"""
        
        keyboard = [
            [InlineKeyboardButton("📦 Mahsulotlar", callback_data='products')],
            [InlineKeyboardButton("🗂️ Kategoriyalar", callback_data='categories')],
            [InlineKeyboardButton("🛒 Savatcha", callback_data='cart')],
            [InlineKeyboardButton("📞 Aloqa", callback_data='contact')]
        ]
        
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    async def products_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, name, price, quantity FROM products WHERE quantity > 0 ORDER BY id DESC LIMIT 20')
        products = c.fetchall()
        conn.close()
        
        if not products:
            await update.message.reply_text("📭 Hozircha mahsulotlar mavjud emas.\n\nAdmin panel orqali mahsulot qo'shing: http://46.101.172.299:5000")
            return
        
        text = "📦 *Mavjud mahsulotlar:*\n\n"
        keyboard = []
        
        for prod_id, name, price, qty in products:
            text += f"• *{name}*\n  💰 {price:,} so'm | 📦 {qty} dona\n\n"
            keyboard.append([InlineKeyboardButton(f"{name} - {price:,} so'm", callback_data=f'view_{prod_id}')])
        
        keyboard.append([InlineKeyboardButton("🛒 Savatcha", callback_data='cart'), InlineKeyboardButton("🏠 Menyu", callback_data='menu')])
        
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    async def categories_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT DISTINCT category FROM products WHERE category IS NOT NULL')
        categories = [row[0] for row in c.fetchall()]
        conn.close()
        
        if not categories:
            await update.message.reply_text("📭 Kategoriyalar mavjud emas")
            return
        
        text = "🗂️ *Kategoriyalar:*\n\n"
        keyboard = []
        
        for category in categories[:8]:
            text += f"• {category}\n"
            keyboard.append([InlineKeyboardButton(f"📁 {category}", callback_data=f'cat_{category}')])
        
        keyboard.append([InlineKeyboardButton("📦 Barcha mahsulotlar", callback_data='products')])
        
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    async def cart_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''SELECT c.id, p.name, p.price, c.quantity 
                     FROM cart c 
                     JOIN products p ON c.product_id = p.id 
                     WHERE c.user_id = ?''', (user_id,))
        cart_items = c.fetchall()
        conn.close()
        
        if not cart_items:
            await update.message.reply_text("🛒 Savatchangiz bo'sh")
            return
        
        text = "🛒 *Savatchangiz:*\n\n"
        total = 0
        keyboard = []
        
        for item_id, name, price, qty in cart_items:
            item_total = price * qty
            total += item_total
            text += f"• {name}\n  {qty} × {price:,} = {item_total:,} so'm\n  ❌ /remove_{item_id}\n\n"
            keyboard.append([InlineKeyboardButton(f"➖ {name}", callback_data=f'dec_{item_id}'), 
                           InlineKeyboardButton(f"➕ {name}", callback_data=f'inc_{item_id}')])
        
        text += f"💰 *Jami:* {total:,} so'm\n\n"
        keyboard.append([InlineKeyboardButton("✅ Buyurtma berish", callback_data='checkout')])
        keyboard.append([InlineKeyboardButton("🗑️ Savatchani tozalash", callback_data='clear_cart'), 
                        InlineKeyboardButton("🏠 Menyu", callback_data='menu')])
        
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    async def myorders_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, total, status, created_at FROM orders WHERE customer_id = ? ORDER BY id DESC LIMIT 10', (user_id,))
        orders = c.fetchall()
        conn.close()
        
        if not orders:
            await update.message.reply_text("📭 Sizda hali buyurtmalar yo'q")
            return
        
        text = "📋 *Sizning buyurtmalaringiz:*\n\n"
        for order_id, total, status, created_at in orders:
            status_icon = "⏳" if status == 'pending' else "🔄" if status == 'processing' else "✅"
            text += f"{status_icon} *Buyurtma #{order_id}*\n💰 {total:,} so'm | 📅 {created_at[:10]}\n\n"
        
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("📦 Mahsulotlar", callback_data='products')],
            [InlineKeyboardButton("🗂️ Kategoriyalar", callback_data='categories')],
            [InlineKeyboardButton("🛒 Savatcha", callback_data='cart')],
            [InlineKeyboardButton("📋 Mening buyurtmalarim", callback_data='my_orders')],
            [InlineKeyboardButton("📍 Filiallar", callback_data='branches'), InlineKeyboardButton("📞 Aloqa", callback_data='contact')]
        ]
        await update.message.reply_text("🏠 *Asosiy menyu:*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    async def callback_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data
        
        if data == 'products':
            await self.products_command(query, context)
        elif data == 'categories':
            await self.categories_command(query, context)
        elif data == 'cart':
            await self.cart_command(query, context)
        elif data == 'menu':
            await self.menu_command(query, context)
        elif data == 'my_orders':
            await self.myorders_command(query, context)
        elif data == 'branches':
            await query.edit_message_text("📍 *Filiallarimiz:*\n\n🏢 Toshkent, Chorsu\n🏢 Samarqand, Registon\n🏢 Buxoro, Lyabi Hauz\n\n🕐 9:00-18:00\n📞 +998 90 123 45 67", parse_mode='Markdown')
        elif data == 'contact':
            await query.edit_message_text("📞 *Aloqa:*\n\n📱 +998 90 123 45 67\n📧 info@mixart.uz\n🤖 @mixart_support\n\n🕐 Ish vaqti: 9:00-18:00", parse_mode='Markdown')
        elif data.startswith('view_'):
            product_id = data.split('_')[1]
            await self.show_product(query, product_id)
        elif data.startswith('cat_'):
            category = data.split('_')[1]
            await self.show_category_products(query, category)
        elif data == 'checkout':
            await self.checkout(query)
        elif data == 'clear_cart':
            await self.clear_cart(query)
    
    async def show_product(self, query, product_id):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT name, price, quantity, category FROM products WHERE id = ?', (product_id,))
        product = c.fetchone()
        conn.close()
        
        if not product:
            await query.edit_message_text("❌ Mahsulot topilmadi")
            return
        
        name, price, qty, category = product
        text = f"""📦 *{name}*

💰 Narxi: {price:,} so'm
📦 Qoldiq: {qty} dona
🗂️ Kategoriya: {category}

{name} ni savatchaga qo'shmoqchimisiz?
"""
        
        keyboard = [
            [InlineKeyboardButton("🛒 Savatchaga qo'shish", callback_data=f'add_{product_id}')],
            [InlineKeyboardButton("📦 Barcha mahsulotlar", callback_data='products'),
             InlineKeyboardButton("🏠 Menyu", callback_data='menu')]
        ]
        
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    async def show_category_products(self, query, category):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, name, price FROM products WHERE category = ? AND quantity > 0', (category,))
        products = c.fetchall()
        conn.close()
        
        if not products:
            await query.edit_message_text(f"📭 '{category}' kategoriyasida mahsulot yo'q")
            return
        
        text = f"🗂️ *{category}*\n\n"
        keyboard = []
        
        for prod_id, name, price in products:
            text += f"• {name} - {price:,} so'm\n"
            keyboard.append([InlineKeyboardButton(f"{name} - {price:,} so'm", callback_data=f'view_{prod_id}')])
        
        keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data='categories')])
        
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    async def checkout(self, query):
        user_id = query.from_user.id
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''SELECT p.name, p.price, c.quantity 
                     FROM cart c 
                     JOIN products p ON c.product_id = p.id 
                     WHERE c.user_id = ?''', (user_id,))
        cart_items = c.fetchall()
        
        if not cart_items:
            await query.edit_message_text("🛒 Savatchangiz bo'sh")
            conn.close()
            return
        
        total = sum(price * qty for _, price, qty in cart_items)
        products_list = [{'name': name, 'price': price, 'quantity': qty} for name, price, qty in cart_items]
        
        # Telefon so'rash
        await query.edit_message_text(f"🛍️ *Buyurtma:*\n\nJami: {total:,} so'm\n\n📱 Iltimos, telefon raqamingizni yuboring:")
        
        context = query.message.chat.id
        context.user_data['checkout_data'] = {
            'products': products_list,
            'total': total
        }
        
        conn.close()
    
    async def clear_cart(self, query):
        user_id = query.from_user.id
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        await query.edit_message_text("✅ Savatcha tozalandi")
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        user_id = update.effective_user.id
        
        if 'checkout_data' in context.user_data:
            # Telefon raqami kiritildi
            if 'phone' not in context.user_data:
                context.user_data['phone'] = text
                await update.message.reply_text("✅ Telefon raqamingiz qabul qilindi!\n\n📍 Manzilingizni yuboring:")
            else:
                # Manzil kiritildi
                address = text
                phone = context.user_data['phone']
                checkout_data = context.user_data['checkout_data']
                
                # Buyurtmani saqlash
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                
                c.execute('''INSERT INTO orders (customer_id, products, total, phone, address) 
                           VALUES (?, ?, ?, ?, ?)''',
                         (user_id, json.dumps(checkout_data['products']), checkout_data['total'], phone, address))
                order_id = c.lastrowid
                
                # Savatchani tozalash
                c.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
                conn.commit()
                conn.close()
                
                # To'lov usullari
                keyboard = [
                    [InlineKeyboardButton("💳 Click", callback_data=f'pay_click_{order_id}'),
                     InlineKeyboardButton("💳 Payme", callback_data=f'pay_payme_{order_id}')],
                    [InlineKeyboardButton("💳 Terminal", callback_data=f'pay_terminal_{order_id}'),
                     InlineKeyboardButton("💰 Naqd", callback_data=f'pay_cash_{order_id}')]
                ]
                
                response = f"""✅ *Buyurtma qabul qilindi!*

🆔 Buyurtma raqami: #{order_id}
💰 Jami summa: {checkout_data['total']:,} so'm
📱 Telefon: {phone}
📍 Manzil: {address}

💳 *To'lov usulini tanlang:*
"""
                await update.message.reply_text(response, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
                
                # Ma'lumotlarni tozalash
                context.user_data.clear()
        
        # Mahsulotni o'chirish komandasi
        elif text.startswith('/remove_'):
            try:
                cart_id = int(text.split('_')[1])
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute('DELETE FROM cart WHERE id = ? AND user_id = ?', (cart_id, user_id))
                conn.commit()
                conn.close()
                await update.message.reply_text("✅ Mahsulot savatchadan olib tashlandi")
            except:
                await update.message.reply_text("❌ Xatolik yuz berdi")
    
    def run(self):
        print("🤖 Mixart Bot ishga tushmoqda...")
        self.application.run_polling()

if __name__ == '__main__':
    TOKEN_FILE = '/root/mixart/config/bot_token.txt'
    
    if not os.path.exists(TOKEN_FILE):
        print("❌ Token fayli topilmadi!")
        exit(1)
    
    with open(TOKEN_FILE, 'r') as f:
        token = f.read().strip()
    
    bot = MixartBot(token)
    bot.run()
