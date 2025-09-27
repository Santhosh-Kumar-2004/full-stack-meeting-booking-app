from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List

import os
from dotenv import load_dotenv

load_dotenv()

# password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
