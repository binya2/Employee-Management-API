from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    office_name: str
    job_title: str

class EmployeeCreate(EmployeeBase):
    id: str

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    office_name: Optional[str] = None
    job_title: Optional[str] = None

class EmployeeResponse(EmployeeBase):
    id: str
    created_at: datetime
    updated_at: datetime

