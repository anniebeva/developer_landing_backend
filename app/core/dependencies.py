from fastapi import Request, HTTPException

from app.core.rate_limit import check_rate_limit


async def rate_limit_dependency(request: Request):
    """Protect endpoint from excessive requests."""

    client_ip = request.client.host

    if not check_rate_limit(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Try again later.",
        )
