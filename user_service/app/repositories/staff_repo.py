from sqlalchemy.orm import Session
from app.repositories.base_repo import BaseRepository
from app.models.staff import Staff

class StaffRepository(BaseRepository[Staff]):
    def __init__(self):
        super().__init__(Staff)

staff_repo = StaffRepository()
