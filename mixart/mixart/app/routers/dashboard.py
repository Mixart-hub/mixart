from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.analytics import daily_sales_chart
from app.services.monthly_analytics import monthly_sales_chart
from app.services.top_products import top_products_chart

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "daily": daily_sales_chart(),
            "monthly": monthly_sales_chart(),
            "top": top_products_chart(),
        }
    )
