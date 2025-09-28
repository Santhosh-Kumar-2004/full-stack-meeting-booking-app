from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Router files
from routers import users, bookings

# Create FastAPI app
app = FastAPI(
    title="Meeting Booking API",
    description="Backend API for managing users and bookings",
    version="1.0.0"
)