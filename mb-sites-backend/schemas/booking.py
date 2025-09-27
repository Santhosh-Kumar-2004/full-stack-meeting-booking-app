from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# For creating booking (input)
class BookingCreate(BaseModel):
    guest_name: str
    guest_email: EmailStr
    reason: str
    meeting_time: datetime

# For showing booking (output)
class BookingResponse(BaseModel):
    id: str
    guest_name: str
    guest_email: EmailStr
    reason: str
    meeting_time: datetime
    created_at: datetime
    user_id: str

    class Config:
        from_attributes = True
