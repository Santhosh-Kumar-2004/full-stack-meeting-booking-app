from pydantic import BaseModel, EmailStr, constr
from typing import Optional

# For user registration (input)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# For login (input)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    
class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True  # allows ORM to Pydantic conversion
