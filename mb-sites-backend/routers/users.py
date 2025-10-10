import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from helper.database import get_db
from helper.auth_utils import ADMIN_EMAILS, create_access_token, get_current_user, verify_password, hash_password
from schemas.user import UserCreate, UserLogin, UserResponse
from models.models import User

router = APIRouter(prefix="/auth", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MAX_PASSWORD_LENGTH = 72  # bcrypt limit

# Register User - 1
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
                detail="Email is already registered"
            )
        
        # hash password
        hashed_password = hash_password(user.password)

         # Decide role
        role = "admin" if user.email.lower() in [email.lower() for email in ADMIN_EMAILS] else "user"


        new_user = User(
            id=str(uuid.uuid4()),
            email=user.email,
            password=hashed_password,
            name=user.name,
            role=role
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


# Login User - 2
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

        access_token = create_access_token(
            email=db_user.email,
            role=db_user.role
        )

        return {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )


# Get all users - 3
@router.get("/", response_model=list[UserResponse]) #only used and viewed by the ADMIN
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves a list of all users from the database.

    Returns:
        list[UserResponse]: A list of all user objects.

    Raises:
        HTTPException 500: Unexpected server or database error.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )

    try:
        users = db.query(User).all()
        return users
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {str(e)}"
        )
