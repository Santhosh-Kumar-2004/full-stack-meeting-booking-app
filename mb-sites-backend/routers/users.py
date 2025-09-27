from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from helper.database import get_db
from helper.auth_utils import create_access_token, verify_password, hash_password
from schemas.user import UserCreate, UserLogin, UserResponse
from models.models import User

router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Register User
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    """
    Registers a new user.

    Checks if the email is already in use. If not, it hashes the password,
    creates a new user record in the database, and returns the newly created user object.

    Raises:
        HTTPException 400: If the email is already registered.
        HTTPException 500: For unexpected server or database errors.
    """

    try:
        db_user = db.query(User).filter(User.email == user.email).first()

        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email address is Invalid"
            )
        
        # hash password
        hashed_password = hash_password(user.password)
        new_user = User(
            email=user.email,
            password=hashed_password,
            full_name=user.name
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


# Login User
@router.post("/login")
def login_user(
    user: UserLogin, 
    db: Session = Depends(get_db)
):
    """
    Authenticates user credentials (email and password).

    If successful, it generates and returns a JWT access token.

    Raises:
        HTTPException 401: Invalid email or password.
        HTTPException 500: Unexpected login error.
    """
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user or not verify_password(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = create_access_token(data={"sub": db_user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )


# Get all users
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {str(e)}"
        )
