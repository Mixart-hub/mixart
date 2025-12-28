import matplotlib.pyplot as plt
import base64
from io import BytesIO

def monthly_sales_chart():
    months = ["Yan", "Fev", "Mar", "Apr", "May", "Iyun"]
    sales = [1200, 1500, 1800, 1700, 2100, 2500]

    plt.figure()
    plt.bar(months, sales)
    plt.title("Oylik savdo")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return base64.b64encode(buf.read()).decode("utf-8")
