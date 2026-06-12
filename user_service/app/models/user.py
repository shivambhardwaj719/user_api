from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    image = Column(String, nullable=True)
    full_name = Column(String(80), nullable=False)
    country_number_code = Column(Integer, default=91)
    phone_number = Column(String(15), nullable=False)
    gender = Column(String(50), nullable=False)
    is_enabled = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    mpin = Column(Integer, nullable=True)
    account_type = Column(String(32), default='sub_admin')
    auth_token_issued_at = Column(DateTime(timezone=True), default=func.now())
    fcm_token = Column(String(255), nullable=True)
    staff = relationship("Staff", back_populates="user", uselist=False)

    @property
    def is_super_admin(self):
        return self.account_type == 'super_admin'