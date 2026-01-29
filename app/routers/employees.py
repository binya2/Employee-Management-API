from fastapi import APIRouter, HTTPException

from app.database import db
from app.models import Employee, EmployeeCreate, EmployeeResponse, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("", response_model=list[EmployeeResponse])
def get_employees():
    return [e.to_dict() for e in db.get_all_employees()]


@router.get("/{emp_id}", response_model=EmployeeResponse)
def get_employee(emp_id: str):
    emp = db.get_employee_by_id(emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp.to_dict()


@router.post("", response_model=EmployeeResponse)
def create_employee(emp: EmployeeCreate):
    if db.get_employee_by_id(emp.id):
        raise HTTPException(status_code=400, detail="Employee ID already exists")

    new_emp = Employee(emp.id, emp.first_name, emp.last_name, emp.office_name, emp.job_title)
    return db.add_employee(new_emp).to_dict()


@router.put("/{emp_id}", response_model=EmployeeResponse)
def update_employee(emp_id: str, emp_update: EmployeeUpdate):
    updated = db.update_employee(emp_id, emp_update.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated.to_dict()


@router.delete("/{emp_id}")
def delete_employee(emp_id: str):
    if not db.delete_employee(emp_id):
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted"}
