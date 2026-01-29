from fastapi import APIRouter

from app.database import db
from app.models import Analytics

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/employees")
def get_employee_stats():
    return Analytics.get_employee_statistics(db.employees)


@router.get("/missions")
def get_mission_stats():
    return Analytics.get_mission_statistics(db.missions)


@router.get("/workload")
def get_workload():
    return Analytics.get_employee_workload(db.employees, db.missions)


@router.get("/summary")
def get_summary():
    return {
        "employees": Analytics.get_employee_statistics(db.employees),
        "missions": Analytics.get_mission_statistics(db.missions)
    }
