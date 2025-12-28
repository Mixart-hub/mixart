from reportlab.pdfgen import canvas
import sqlite3
db=sqlite3.connect('data/mixart.db')
c=db.cursor()
c.execute("SELECT SUM(amount) FROM orders")
total=c.fetchone()[0] or 0
pdf=canvas.Canvas("reports/daily.pdf")
pdf.drawString(100,800,f"Kunlik savdo: {total}")
pdf.save()
