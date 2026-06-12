from sqlalchemy.orm import Session
from app.repositories.user_repo import user_repo
from app.schemas.user import UserCreate, UserUpdate
from app.utils.response.handlers import ResponseHandler
from app.utils.response.messages import ResponseMessages
from app.utils.notifications.firebase import send_multicast_notification

class UserService:
    @staticmethod
    def create_user(db: Session, request: UserCreate):
        existing = user_repo.get_by_email(db, request.email)
        if existing:
            return ResponseHandler.create_failed(message=ResponseMessages.USER_ALREADY_EXISTS.format(name=existing.full_name))

        user_data = request.model_dump()
        user_data['hashed_password'] = user_data.pop('password')
        
        new_user = user_repo.create(db, user_data)
        
        super_admins = user_repo.get_all(db, account_type="super_admin")
        fcm_tokens = [admin.fcm_token for admin in super_admins if admin.fcm_token]
        
        if fcm_tokens:
            send_multicast_notification(
                tokens=fcm_tokens,
                title=ResponseMessages.NEW_USER_CREATED_TITLE,
                body=ResponseMessages.NEW_USER_CREATED_BODY.format(name=new_user.full_name)
            )
            
        return ResponseHandler.create_success(name="User")

    @staticmethod
    def get_user(db: Session, user_id: int):
        user = user_repo.get(db, user_id)
        if not user:
            return ResponseHandler.no_matching_data()
        return user

    @staticmethod
    def update_user(db: Session, user_id: int, request: UserUpdate):
        user = user_repo.get(db, user_id)
        if not user:
            return ResponseHandler.no_matching_data()
        
        update_data = request.model_dump(exclude_unset=True)
        if 'is_enabled' in update_data:
            update_data['is_active'] = update_data['is_enabled']
            
        user_repo.update(db, user, update_data)
        return ResponseHandler.update_success('User')

    @staticmethod
    def delete_users(db: Session, ids: list[int]):
        for uid in ids:
            user_repo.delete(db, uid)
        return ResponseHandler.delete_success('User')

user_service = UserService()
