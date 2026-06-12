from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_db, get_current_user
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserStatusAction
from app.models.user import User
from app.services.user_service import user_service
from app.repositories.user_repo import user_repo
from app.utils.response.handlers import ResponseHandler
from app.utils.response.messages import ResponseMessages

router = APIRouter()

@router.post("/", response_model=None)
def create_user(request: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_service.create_user(db, request)

@router.get("/", response_model=None)
def list_users(
    search: Optional[str] = None, 
    account_type: Optional[str] = None,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    users = user_repo.get_all(db) # We should add filters properly, but keeping it simple for the refactor
    filtered_users = [u for u in users if u.id != current_user.id]
    
    if search:
        search = search.lower()
        filtered_users = [u for u in filtered_users if search in u.full_name.lower() or search in u.email.lower()]
    
    if account_type:
        filtered_users = [u for u in filtered_users if u.account_type == account_type]

    data = [UserResponse.model_validate(u).model_dump() for u in filtered_users]
    return ResponseHandler.list_success(data)

@router.get("/{id}", response_model=None)
def get_user(id: int = Path(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = user_service.get_user(db, id)
    if isinstance(user, dict) and not user.get('success'): # If it's an error response dict
        return user
    if not isinstance(user, User):
        return user
    return ResponseHandler.list_success(UserResponse.model_validate(user).model_dump())

@router.put("/{id}", response_model=None)
def update_user(
    id: int, 
    request: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return user_service.update_user(db, id, request)

@router.delete("/", response_model=None)
def delete_user(ids: List[int], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not ids:
        return ResponseHandler.delete_success("None")
    return user_service.delete_users(db, ids)

@router.patch("/{id}/status", response_model=None)
def change_status(id: int, request: UserStatusAction, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = user_repo.get(db, id)
    if not user:
        return ResponseHandler.not_found()

    if request.action not in ['enable', 'disable']:
        return ResponseHandler.bad_request(message="Invalid action. Use 'enable' or 'disable'.")

    user_repo.update(db, user, {'is_enabled': request.action == 'enable', 'is_active': request.action == 'enable'})
    return ResponseHandler.success()
