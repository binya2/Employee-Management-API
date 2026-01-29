from fastapi import APIRouter, HTTPException

from app.database import db
from app.models import Mission, MissionCreate, MissionResponse

router = APIRouter(prefix="/missions", tags=["missions"])


@router.get("", response_model=list[MissionResponse])
def get_all_mission():
    return [m.to_dict() for m in db.get_all_missions()]


@router.get("/{mission_id}", response_model=MissionResponse)
def get_mission_by_id(mission_id):
    mission = db.get_mission_by_id(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission.to_dict()


@router.post("", response_model=MissionResponse)
def create_new_mission(mission: MissionCreate):
    if db.get_mission_by_id(mission.id):
        raise HTTPException(status_code=400, detail="Mission ID already exists")

    if not db.get_employee_by_id(mission.assigned_to):
        raise HTTPException(status_code=400, detail="Assigned employee does not exist")

    new_mission = Mission(mission.id, mission.title, mission.assigned_to, mission.status, mission.priority,
                          mission.deadline)
    return db.add_mission(new_mission).to_dict()


@router.put('/missions/{mission_id}')
def update_mission(mission_id, MissionUpdate):
    pass


@router.delete('/missions/{mission_id}')
def delete_mission(mission_id):
    pass


@router.get("/employee/{emp_id}", response_model=list[MissionResponse])
def get_missions_by_employee(emp_id):
    return [m.to_dict() for m in db.get_missions_by_employee(emp_id)]
