from fastapi import APIRouter, HTTPException
from app.models import EmployeeCreate, EmployeeUpdate
from app.database import Database

router = APIRouter()
db = Database()

db.init_sample_data()

@router.get("/employees")
def get_employees():
    return db.get_all_employees()

@router.get("/employees/{emp_id}")
def get_employee(emp_id: str):
    employee = db.get_employee_by_id(emp_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.post("/employees")
def create_employee(employee: EmployeeCreate):
    return db.add_employee(employee)

@router.put("/employees/{emp_id}")
def update_employee(emp_id: str, employee_data: EmployeeUpdate):
    employee = db.update_employee(emp_id, employee_data)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.delete("/employees/{emp_id}")
def delete_employee(emp_id: str):
    success = db.delete_employee(emp_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"detail": "Employee deleted"}