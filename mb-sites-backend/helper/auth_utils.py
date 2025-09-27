from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from helper.database import get_db
from models.models import User

import os
from dotenv import load_dotenv

load_dotenv()

# password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#JWT settings added
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_EXPIRE_MINUTES")

# Admins email, RBAC (from .env)
ADMIN_EMAILS = os.getenv("ADMIN_EMAILS", "").split(",")


# ---------------- PASSWORD UTILS ----------------

def hash_password(password: str) -> str:
    """
    Hash a plain password using bcrypt and make it unreadable
    """

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against the hashed password, which is taken from the DB
    """

    return pwd_context.verify(plain_password, hashed_password)


# ---------------- JWT UTILS ----------------

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT token with expiration of 60 minutes.
    """

    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt 


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode JWT token and return payload if valid
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    
    except JWTError:
        return None
    


# ---------------- ROLE CHECK ----------------

def is_admin(email: str) -> bool:
    """
    Check if a given email is an admin
    """

    return email in ADMIN_EMAILS


# ✅ Dependency to get current logged-in user
def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email: str = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload invalid (missing sub)",
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user  # returns full User ORM object