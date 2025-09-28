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

# Middleware (CORS for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Change to specific frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(users.router)
app.include_router(bookings.router)