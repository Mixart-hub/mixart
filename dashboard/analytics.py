import base64
from io import BytesIO
import matplotlib.pyplot as plt

def daily_sales_chart():
    days = ["Du", "Se", "Ch", "Pa", "Ju", "Sh", "Ya"]
    sales = [120, 150, 90, 180, 200, 170, 220]

    plt.figure()
    plt.plot(days, sales, marker="o")
    plt.title("Kunlik savdo")
    plt.xlabel("Kunlar")
    plt.ylabel("Savdo")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return base64.b64encode(buf.read()).decode("utf-8")
