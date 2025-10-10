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
# Admin emails (turns into Python list)
ADMIN_EMAILS = os.getenv("ADMIN_EMAILS", "").split(",")
ADMIN_EMAILS = [email.strip().lower() for email in os.getenv("ADMIN_EMAILS", "").split(",") if email.strip()]


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

def create_access_token(email: str, role: str, expires_delta: timedelta = None) -> str:
    to_encode = {
        "sub": email,
        "role": role,
        "exp": datetime.utcnow() + (expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



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

def is_admin(db: Session, email: str) -> bool:
    user = db.query(User).filter(User.email == email).first()
    return user and user.role == "admin"



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
        )

    email = payload.get("sub")
    role = payload.get("role")

    if not email:
        raise HTTPException(status_code=401, detail="Token missing email (sub)")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # keep DB role in sync (optional but smart)
    if email.lower() in ADMIN_EMAILS and user.role != "admin":
        user.role = "admin"
        db.commit()
        db.refresh(user)

    # attach role from token if exists
    user.role = role or user.role

    return user
