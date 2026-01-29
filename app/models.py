from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel
from enum import Enum


# --- Employee Models ---
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


class Employee:
    def __init__(self, id, first_name, last_name, office_name, job_title):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.office_name = office_name
        self.job_title = job_title
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "office_name": self.office_name,
            "job_title": self.job_title,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


# --- Mission Models ---
class MissionStatus(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class MissionPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class MissionBase(BaseModel):
    title: str
    assigned_to: str
    status: MissionStatus
    priority: MissionPriority
    deadline: str


class MissionCreate(MissionBase):
    id: str


class MissionUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[MissionStatus] = None
    priority: Optional[MissionPriority] = None
    deadline: Optional[str] = None


class MissionResponse(MissionBase):
    id: str
    created_at: datetime


class Mission:
    def __init__(self, id, title, assigned_to, status, priority, deadline):
        self.id = id
        self.title = title
        self.assigned_to = assigned_to
        self.status = status
        self.priority = priority
        self.deadline = deadline
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "priority": self.priority,
            "deadline": self.deadline,
            "created_at": self.created_at
        }


# --- Analytics Model ---
class Analytics:
    @staticmethod
    def get_employee_statistics(employees: List[Employee]):
        total = len(employees)
        by_office = {}
        by_job = {}

        for emp in employees:
            by_office[emp.office_name] = by_office.get(emp.office_name, 0) + 1
            by_job[emp.job_title] = by_job.get(emp.job_title, 0) + 1

        return {
            "total_employees": total,
            "by_office": by_office,
            "by_job_title": by_job
        }

    @staticmethod
    def get_mission_statistics(missions: List[Mission]):
        total = len(missions)
        by_status = {}
        by_priority = {}

        for m in missions:
            by_status[m.status] = by_status.get(m.status, 0) + 1
            by_priority[m.priority] = by_priority.get(m.priority, 0) + 1

        return {
            "total_missions": total,
            "by_status": by_status,
            "by_priority": by_priority
        }

    @staticmethod
    def get_employee_workload(employees: List[Employee], missions: List[Mission]):
        workload = []
        for emp in employees:
            emp_missions = [m for m in missions if m.assigned_to == emp.id]
            active = len([m for m in emp_missions if m.status in ["Pending", "In Progress"]])
            completed = len([m for m in emp_missions if m.status == "Completed"])

            workload.append({
                "employee_id": emp.id,
                "name": f"{emp.first_name} {emp.last_name}",
                "total_missions": len(emp_missions),
                "active_missions": active,
                "completed_missions": completed
            })
        return workload
