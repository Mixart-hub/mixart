import base64
from io import BytesIO
import matplotlib.pyplot as plt

def top_products_chart():
    products = ["A", "B", "C", "D"]
    sales = [120, 90, 60, 30]

    plt.figure()
    plt.bar(products, sales)
    plt.title("Top mahsulotlar")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return base64.b64encode(buf.read()).decode("utf-8")
