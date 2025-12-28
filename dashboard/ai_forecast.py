import matplotlib.pyplot as plt
import numpy as np
import os

def ai_sales_forecast():
    days = np.arange(1, 8)
    forecast = [150, 160, 170, 180, 190, 200, 210]

    os.makedirs("static/charts", exist_ok=True)
    path = "static/charts/forecast.png"

    plt.figure()
    plt.plot(days, forecast, marker="o")
    plt.title("AI sotuv bashorati")
    plt.xlabel("Kunlar")
    plt.ylabel("Sotuv")
    plt.savefig(path)
    plt.close()

    return "/static/charts/forecast.png"
