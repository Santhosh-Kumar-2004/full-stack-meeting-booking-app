from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List

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