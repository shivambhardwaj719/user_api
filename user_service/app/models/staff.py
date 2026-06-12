from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Numeric, Text
from sqlalchemy.orm import relationship
from .base import Base

class Staff(Base):
    __tablename__ = "staffs"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(Text, nullable=True)
    person_name = Column(String(100), nullable=False)
    gender = Column(String(100), nullable=False)
    phone_number = Column(String(100), nullable=False)
    official_email_id = Column(String(255), nullable=True)
    personal_email_id = Column(String(255), nullable=False)
    date_of_joining = Column(Date, nullable=False)
    staff_type = Column(String(20), nullable=False)
    is_enabled = Column(Boolean, default=True)
    deleted_by = Column(String(255), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="staff")
