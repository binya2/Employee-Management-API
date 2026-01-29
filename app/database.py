from typing import List, Optional
from app.models import EmployeeBase, EmployeeCreate, EmployeeUpdate, Mission, MissionUpdate

class Database:
    employees: List[EmployeeBase] = []
    missions: List[Mission] = []

    def add_employee(self, employee: EmployeeCreate): 
        self.employees.append(employee)
        return employee

    def get_all_employees(self) -> List[EmployeeBase]:
        return self.employees

    def get_employee_by_id(self, emp_id: str) -> Optional[EmployeeBase]:
        for employee in self.employees:
            if employee.id == emp_id:
                return employee

    def update_employee(self, emp_id: str, data: EmployeeUpdate) -> Optional[EmployeeBase]:
        employee = self.get_employee_by_id(emp_id)
        if not employee:
            return None
        update_dict = data.model_dump(exclude_unset=True)
        if "first_name" in update_dict:
            employee.first_name = update_dict["first_name"]
        if "last_name" in update_dict:
            employee.last_name = update_dict["last_name"]
        if "office_name" in update_dict:
            employee.office_name = update_dict["office_name"]
        if "job_title" in update_dict:
            employee.job_title = update_dict["job_title"]

        return employee

    def delete_employee(self, emp_id: str) -> bool:
        employee = self.get_employee_by_id(emp_id)
        if employee:
            self.employees.remove(employee)
            return True
        return False

    def init_sample_data(self):
        sample_employees = [
            EmployeeCreate(first_name="John", last_name="Doe", office_name="New York", job_title="Developer", id="1"),
            EmployeeCreate(first_name="Jane", last_name="Smith", office_name="London", job_title="Designer", id="2"),
            EmployeeCreate(first_name="Alice", last_name="Johnson", office_name="Sydney", job_title="Manager", id="3"),
        ]
        self.employees.extend(sample_employees)

    
    def add_mission(self, mission: Mission): 
        self.missions.append(mission)
        return mission
    

    def get_all_missions(self) -> List[Mission]:
        return self.missions
    
    def get_mission_by_id(self, mission_id) -> Optional[Mission]:
        for mission in self.missions: 
            if mission.id == mission_id:
                return mission
            
    
    def get_missions_by_employee(self, emp_id) -> Optional[Mission]:
        for mission in self.missions:
            for emp in self.employees:
                pass