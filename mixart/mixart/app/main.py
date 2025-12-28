from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers.dashboard import router as dashboard_router

app = FastAPI(title="Mixart Analytics")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(dashboard_router)
