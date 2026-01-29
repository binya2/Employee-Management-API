from datetime import datetime
from typing import List, Optional
from app.models import Employee, Mission


class Database:
    def __init__(self):
        self.employees: List[Employee] = []
        self.missions: List[Mission] = []
        self.init_sample_data()

    def init_sample_data(self):
        self.employees.append(Employee("E001", "John", "Smith", "Headquarters", "Software Engineer"))
        self.employees.append(Employee("E002", "Sarah", "Johnson", "Regional Office", "Project Manager"))
        self.employees.append(Employee("E003", "Michael", "Williams", "Headquarters", "Data Analyst"))
        self.employees.append(Employee("E004", "Emily", "Brown", "Branch Office", "HR Specialist"))

        self.missions.append(Mission("M001", "Develop API Docs", "E001", "In Progress", "High", "2024-12-31"))
        self.missions.append(Mission("M002", "DB Migration", "E003", "Pending", "Medium", "2024-12-15"))
        self.missions.append(Mission("M003", "Security Audit", "E002", "Completed", "High", "2024-11-30"))
        self.missions.append(Mission("M004", "Perf Testing", "E001", "In Progress", "Critical", "2024-12-20"))

    def add_employee(self, employee: Employee) -> Employee:
        self.employees.append(employee)
        return employee

    def get_all_employees(self) -> List[Employee]:
        return self.employees

    def get_employee_by_id(self, emp_id: str) -> Optional[Employee]:
        return next((e for e in self.employees if e.id == emp_id), None)

    def update_employee(self, emp_id: str, data: dict) -> Optional[Employee]:
        emp = self.get_employee_by_id(emp_id)
        if emp:
            if data.get('first_name'): emp.first_name = data['first_name']
            if data.get('last_name'): emp.last_name = data['last_name']
            if data.get('office_name'): emp.office_name = data['office_name']
            if data.get('job_title'): emp.job_title = data['job_title']
            emp.updated_at = datetime.now()
        return emp

    def delete_employee(self, emp_id: str) -> bool:
        initial_len = len(self.employees)
        self.employees = [e for e in self.employees if e.id != emp_id]
        return len(self.employees) < initial_len

    def add_mission(self, mission: Mission) -> Mission:
        self.missions.append(mission)
        return mission

    def get_all_missions(self) -> List[Mission]:
        return self.missions

    def get_mission_by_id(self, mission_id: str) -> Optional[Mission]:
        return next((m for m in self.missions if m.id == mission_id), None)

    def get_missions_by_employee(self, emp_id: str) -> List[Mission]:
        return [m for m in self.missions if m.assigned_to == emp_id]

    def update_mission(self, mission_id: str, data: dict) -> Optional[Mission]:
        mission = self.get_mission_by_id(mission_id)
        if mission:
            if data.get('title'): mission.title = data['title']
            if data.get('status'): mission.status = data['status']
            if data.get('priority'): mission.priority = data['priority']
            if data.get('deadline'): mission.deadline = data['deadline']
        return mission

    def delete_mission(self, mission_id: str) -> bool:
        initial_len = len(self.missions)
        self.missions = [m for m in self.missions if m.id != mission_id]
        return len(self.missions) < initial_len


db = Database()
