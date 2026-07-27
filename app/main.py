from fastapi import FastAPI

from app.core.config import settings
from app.routers import contact_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend service for developer landing page",
    version="1.0.0",
)


app.include_router(contact_router)


@app.get("/")
async def root():
    return {"message": "Developer Landing Backend is running"}
