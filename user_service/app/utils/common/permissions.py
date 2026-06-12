from fastapi import Depends
from app.api.deps import get_current_user
from app.models.user import User
from app.utils.response.handlers import ResponseHandler

def check_permissions(required_permissions: list[str] = None):
    def permission_checker(current_user: User = Depends(get_current_user)):
        if not required_permissions:
            return current_user
        if current_user.is_super_admin:
            return current_user
            
        user_permissions = [] 
        
        if not any(perm in user_permissions for perm in required_permissions):
            return ResponseHandler.forbidden()
            
        return current_user
        
    return permission_checker
