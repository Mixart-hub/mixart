import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO
from sklearn.linear_model import LinearRegression

def ai_sales_forecast():
    days = np.array([1, 2, 3, 4, 5, 6, 7]).reshape(-1, 1)
    sales = np.array([50, 55, 60, 58, 65, 70, 75])

    model = LinearRegression()
    model.fit(days, sales)

    future_days = np.array([8, 9, 10, 11, 12, 13, 14]).reshape(-1, 1)
    forecast = model.predict(future_days)

    plt.figure()
    plt.plot(days, sales, label="Haqiqiy sotuv")
    plt.plot(future_days, forecast, linestyle="--", label="AI bashorat")
    plt.legend()
    plt.title("AI sotuv bashorati")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return base64.b64encode(buf.read()).decode("utf-8")
