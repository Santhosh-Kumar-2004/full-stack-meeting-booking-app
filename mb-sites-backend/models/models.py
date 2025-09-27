from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from helper.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum("user", "admin"), default="user")



class Booking(Base):
    __tablename__ = "bookings"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    guest_name = Column(String(100), nullable=False)
    guest_email = Column(String(100), nullable=False)
    reason = Column(String(255), nullable=False)
    meeting_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

