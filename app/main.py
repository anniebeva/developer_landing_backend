from fastapi import FastAPI

from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    description="Backend service for developer landing page",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": "Developer Landing Backend is running"
    }