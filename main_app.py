from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def root():
    return {"status": "Mixart working"}


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )


@app.get("/api/stats")
def stats():
    return JSONResponse({
        "users": 1,
        "orders": 0,
        "daily": {
            "labels": ["Du", "Se", "Ch", "Pa", "Ju", "Sh", "Ya"],
            "values": [10, 20, 15, 30, 25, 40, 35]
        },
        "monthly": {
            "labels": ["Yan", "Fev", "Mar", "Apr", "May"],
            "values": [200, 300, 250, 400, 380]
        },
        "top": {
            "labels": ["Mahsulot A", "Mahsulot B", "Mahsulot C"],
            "values": [50, 30, 20]
        }
    })
