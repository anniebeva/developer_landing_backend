import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import ContactCreationError
from app.core.handlers import contact_creation_exception_handler
from app.core.logging import setup_logging
from app.routers import contact_router, health_router, metrics_router

setup_logging()

logger = logging.getLogger(__name__)


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


@app.middleware("http")
async def log_requests(
    request: Request,
    call_next,
):
    """Log incoming HTTP requests."""

    logger.info(
        "Request started: %s %s",
        request.method,
        request.url.path,
    )

    response = await call_next(request)

    logger.info(
        "Request finished: %s %s -> %s",
        request.method,
        request.url.path,
        response.status_code,
    )

    return response


@app.exception_handler(Exception)
async def internal_server_error_handler(
    request: Request,
    exc: Exception,
):
    """Handle unexpected application errors."""

    logger.exception(
        "Unhandled exception",
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
        },
    )


app.include_router(contact_router)
app.include_router(health_router)
app.include_router(metrics_router)


@app.get("/")
async def root():
    """Health check endpoint."""

    return {
        "message": "Developer Landing Backend is running",
    }
