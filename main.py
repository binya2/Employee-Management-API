from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import employees, missions, analysis

app = FastAPI(title="Employee Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(employees.router, prefix="/api")
app.include_router(missions.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Employee Management API",
        "endpoints": [
            "/api/employees",
            "/api/missions",
            "/api/analysis/summary",
            "/docs"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
