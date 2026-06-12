from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Numeric, Text
from sqlalchemy.orm import relationship
from .base import Base

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    hospital_name = Column(String(255), nullable=False)
    hospital_code = Column(String(50), nullable=False)
    logo = Column(Text, nullable=True)
    established_date = Column(Date, nullable=False)
    about_hospital = Column(Text, nullable=True)
    sub_domain = Column(String(255), unique=True, index=True, nullable=False)
    client_name = Column(String(100), nullable=False)
    client_email = Column(String(255), nullable=False)
    client_number = Column(String(20), nullable=False)
    is_enabled = Column(Boolean, default=True)

    pass

    @property
    def full_domain(self):
        return f"www.{self.sub_domain}.okcare.in"
