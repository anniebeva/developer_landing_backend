from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.schemas import ContactCreate, ContactResponse
from app.services import ContactService


from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Contact"])


@router.post("/contact", response_model=ContactResponse)
async def create_contact(
    contact_data: ContactCreate,
    session: AsyncSession = Depends(get_session),
):
    service = ContactService(session)

    contact = await service.create_contact(contact_data)

    return contact
