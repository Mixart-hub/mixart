from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from dashboard.analytics import daily_sales_chart
from dashboard.monthly_analytics import monthly_sales_chart
from dashboard.top_products import top_products_chart

app = FastAPI()

templates = Jinja2Templates(directory="dashboard/templates")


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    chart = daily_sales_chart()
    chart_month = monthly_sales_chart()
    chart_top = top_products_chart()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "chart": chart,
            "chart_month": chart_month,
            "chart_top": chart_top,
        }
    )
