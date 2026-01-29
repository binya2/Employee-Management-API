from fastapi import APIRouter
from models import MissionCreate, MissionUpdate

router = APIRouter()


@router.get('/missions')
def get_all_mission():
    pass

@router.get('/missions/{mission_id')
def get_mission_by_id(mission_id):
    pass


@router.post('missions')
def create_new_mission(MissionCreate):
    pass


@router.put('/missions/{mission_id}')
def update_mission(mission_id, MissionUpdate):
    pass


@router.delete('/missions/{mission_id}')
def delete_mission(mission_id):
    pass

@router.get('/missions/employee/{emp_id}')
def get_missions_by_employee(emp_id):
    pass


