from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MissionBase(BaseModel):
    title: str
    assigned_to: str
    status: str
    priority: str
    deadline: datetime = Field(default_factory=datetime.now)

class MissionCreate(MissionBase):
    id: int

class MissionUpdate(MissionBase):
    title: Optional[str] = None
    assigned_to: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    deadline: datetime = Field(default_factory=datetime.now)

class MissionResponse(MissionCreate):
    created_at: datetime = Field(default_factory=datetime.now)

class Mission(BaseModel):
    id: str                     
    title: str                                                
    assigned_to: str             
    status: str     
    priority: str                 
    deadline: datetime                                       
    created_at: datetime = Field(default_factory=datetime.now)


    def to_dict(self):
        return self.model_dump()



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


