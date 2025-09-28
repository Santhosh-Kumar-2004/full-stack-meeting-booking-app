from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import users, bookings