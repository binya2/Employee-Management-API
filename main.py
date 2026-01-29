from fastapi import FastAPI
from app.routers import employees

app = FastAPI()

app.include_router(employees.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Employee Management API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}