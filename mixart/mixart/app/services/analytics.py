import matplotlib.pyplot as plt
import io
import base64

def daily_sales_chart():
    days = ["Du", "Se", "Ch", "Pa", "Ju", "Sh", "Ya"]
    sales = [120, 150, 90, 180, 200, 170, 220]

    plt.figure()
    plt.plot(days, sales, marker="o")
    plt.title("Kunlik savdo")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()

    return base64.b64encode(buf.getvalue()).decode()
