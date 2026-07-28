from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ContactCreationError


async def contact_creation_exception_handler(
    request: Request,
    exc: ContactCreationError,
):
    return JSONResponse(
        status_code=500,
        content={"detail": "Failed to create contact request"},
    )
