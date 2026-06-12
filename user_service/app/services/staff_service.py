from sqlalchemy.orm import Session
from app.repositories.staff_repo import staff_repo
from app.repositories.user_repo import user_repo
from app.schemas.staff import StaffCreate, StaffUpdate
from app.utils.response.handlers import ResponseHandler
from app.utils.response.messages import ResponseMessages
from datetime import date
from app.utils.notifications.firebase import send_multicast_notification

class StaffService:
    @staticmethod
    def create_staff(db: Session, request: StaffCreate):
        if request.official_email_id:
            existing = user_repo.get_by_email(db, request.official_email_id)
            if existing:
                return ResponseHandler.create_failed(message=ResponseMessages.USER_ALREADY_EXISTS.format(name=existing.full_name))

        new_user_id = None
        if request.create_user:
            if not request.official_email_id:
                return ResponseHandler.create_failed(message=ResponseMessages.MISSING_EMAIL_FOR_STAFF_USER)
            
            user_data = {
                "full_name": request.person_name,
                "email": request.official_email_id,
                "phone_number": request.phone_number,
                "gender": request.gender,
                "account_type": "sub_admin",
                "hashed_password": "hashed_placeholder"
            }
            new_user = user_repo.create(db, user_data)
            new_user_id = new_user.id
            
            super_admins = user_repo.get_all(db, account_type="super_admin")
            fcm_tokens = [admin.fcm_token for admin in super_admins if admin.fcm_token]
            if fcm_tokens:
                send_multicast_notification(
                    tokens=fcm_tokens,
                    title=ResponseMessages.NEW_STAFF_USER_CREATED_TITLE,
                    body=ResponseMessages.NEW_STAFF_USER_CREATED_BODY.format(name=new_user.full_name)
                )

        staff_data = request.model_dump(exclude={"create_user"})
        staff_data["date_of_joining"] = date.today()
        staff_data["user_id"] = new_user_id
        
        staff_repo.create(db, staff_data)
        
        if request.create_user:
            return ResponseHandler.create_success(name="Staff and User")
        return ResponseHandler.create_success(name="Staff")

    @staticmethod
    def update_staff(db: Session, staff_id: int, request: StaffUpdate):
        staff = staff_repo.get(db, staff_id)
        if not staff or staff.deleted_by:
            return ResponseHandler.no_matching_data()
            
        staff_repo.update(db, staff, request.model_dump(exclude_unset=True))
        return ResponseHandler.update_success('Staff')

staff_service = StaffService()
