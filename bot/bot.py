import os, telebot, sqlite3
from dotenv import load_dotenv
load_dotenv()

bot=telebot.TeleBot(os.getenv("8500197278:AAE0Gzt_FzH4oIRQLo4CXR31Goxw2veaNjM"))

@bot.message_handler(commands=['start'])import sqlite3

def save_user(tid):
    db=sqlite3.connect('data/mixart.db')
    c=db.cursor()
    c.execute("INSERT OR IGNORE INTO users(telegram_id) VALUES(?)",(tid,))
    db.commit()
    db.close()

@bot.message_handler(commands=['start'])
def s(m):
    save_user(m.from_user.id)
    bot.reply_to(m,"✅ Mixart bot ishlayapti")
def s(m): bot.reply_to(m,"✅ Mixart bot ishlayapti")

@bot.message_handler(commands=['order'])
def o(m):
    db=sqlite3.connect('data/mixart.db')
    c=db.cursor()
    c.execute("INSERT INTO orders(amount) VALUES(10000)")
    db.commit()
    bot.reply_to(m,"🧾 Buyurtma qo‘shildi")

bot.infinity_polling()
