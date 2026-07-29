from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.schemas import ContactCreate, ContactResponse
from app.services import ContactService
from app.core.dependencies import rate_limit_dependency

from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Contact"])


@router.post(
    "/contact",
    response_model=ContactResponse,
    dependencies=[
        Depends(rate_limit_dependency),
    ],
)
async def create_contact(
    contact_data: ContactCreate,
    session: AsyncSession = Depends(get_session),
):
    service = ContactService(session)

    contact = await service.create_contact(contact_data)

    return contact
