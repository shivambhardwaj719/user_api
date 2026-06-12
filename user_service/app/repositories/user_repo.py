from sqlalchemy.orm import Session
from app.repositories.base_repo import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> User:
        return db.query(self.model).filter(self.model.email == email).first()

user_repo = UserRepository()
