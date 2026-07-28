from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import ContactCreationError
from app.core.handlers import contact_creation_exception_handler
from app.routers import contact_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend service for developer landing page",
    version="1.0.0",
)


app.add_exception_handler(
    ContactCreationError,
    contact_creation_exception_handler,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(contact_router)


@app.get("/")
async def root():
    return {"message": "Developer Landing Backend is running"}
