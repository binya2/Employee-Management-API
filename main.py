from fastapi import FastAPI
from app.routers import missions 

app = FastAPI()

app.include_router(missions.router, prefix="/api")