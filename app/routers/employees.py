from fastapi import APIRouter, HTTPException

from app.database import db
from app.models import EmployeeCreate, EmployeeUpdate, Employee

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("")
def get_employees():
    return [e.to_dict() for e in db.get_all_employees()]


@router.get("/{emp_id}")
def get_employee(emp_id: str):
    employee = db.get_employee_by_id(emp_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.post("")
def create_employee(employee: EmployeeCreate):
    if db.get_employee_by_id(employee.id):
        raise HTTPException(status_code=400, detail="Employee ID already exists")

    new_emp = Employee(employee.id, employee.first_name, employee.last_name, employee.office_name, employee.job_title)
    return db.add_employee(new_emp).to_dict()


@router.put("/{emp_id}")
def update_employee(emp_id: str, employee_data: EmployeeUpdate):
    employee = db.update_employee(emp_id, employee_data.model_dump(exclude_unset=True))
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.delete("/employees/{emp_id}")
def delete_employee(emp_id: str):
    success = db.delete_employee(emp_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"detail": "Employee deleted"}
