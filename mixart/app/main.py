from fastapi import FastAPI
from app.routers.dashboard import router as dashboard_router

app = FastAPI()

app.include_router(dashboard_router)
