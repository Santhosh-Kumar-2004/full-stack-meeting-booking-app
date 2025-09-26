import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

#Loadin the env variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "meeting_db")

# SQLAlchemy connection URL for MySQL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine for database
engine = create_engine(
    DATABASE_URL, 
    echo=True,
    pool_size=30,
    max_overflow=20
)

# Create session
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()
