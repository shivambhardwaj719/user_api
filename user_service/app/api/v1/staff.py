from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_db, get_current_user
from app.schemas.staff import StaffCreate, StaffUpdate, StaffResponse, StaffActionRequest
from app.models.user import User
from app.services.staff_service import staff_service
from app.repositories.staff_repo import staff_repo
from app.repositories.user_repo import user_repo
from app.utils.response.handlers import ResponseHandler
from app.utils.response.messages import ResponseMessages

router = APIRouter()

@router.post("/", response_model=None)
def create_staff(request: StaffCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return staff_service.create_staff(db, request)

@router.get("/", response_model=None)
def list_staff(
    search: Optional[str] = None, 
    staff_type: Optional[str] = None,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    staffs = staff_repo.get_all(db)
    filtered = [s for s in staffs if s.deleted_by is None and s.user_id != current_user.id]
    
    if search:
        search = search.lower()
        filtered = [s for s in filtered if search in s.person_name.lower()]
    
    if staff_type:
        filtered = [s for s in filtered if s.staff_type == staff_type]

    data = [StaffResponse.model_validate(s).model_dump() for s in filtered]
    return ResponseHandler.list_success(data)

@router.get("/{id}", response_model=None)
def get_staff(id: int = Path(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    staff = staff_repo.get(db, id)
    if not staff or staff.deleted_by:
        return ResponseHandler.no_matching_data()
    return ResponseHandler.list_success(StaffResponse.model_validate(staff).model_dump())

@router.put("/{id}", response_model=None)
def update_staff(
    id: int, 
    request: StaffUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return staff_service.update_staff(db, id, request)

@router.delete("/", response_model=None)
def delete_staff(ids: List[int], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not ids:
        return ResponseHandler.delete_success("None")

    for id in ids:
        staff = staff_repo.get(db, id)
        if staff:
            staff_repo.update(db, staff, {"deleted_by": current_user.full_name})
            
    return ResponseHandler.delete_success('Staff')

@router.patch("/{id}/status", response_model=None)
def change_status(id: int, request: StaffActionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    staff = staff_repo.get(db, id)
    if not staff:
        return ResponseHandler.not_found()

    if request.action not in ['enable', 'disable']:
        return ResponseHandler.bad_request(message=ResponseMessages.INVALID_ACTION)

    is_enabled = request.action == 'enable'
    staff_repo.update(db, staff, {"is_enabled": is_enabled})
    
    if staff.user_id:
        user = user_repo.get(db, staff.user_id)
        if user:
            user_repo.update(db, user, {"is_active": is_enabled})
            
    return ResponseHandler.success()
