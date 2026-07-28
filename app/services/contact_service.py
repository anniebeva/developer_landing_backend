from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contact import ContactRequest
from app.repositories import ContactRepository
from app.schemas import ContactCreate


class ContactService:
    def __init__(self, session: AsyncSession):
        self.repository = ContactRepository(session)

    async def create_contact(self, contact_data: ContactCreate):
        contact = ContactRequest(
            name=contact_data.name,
            phone=contact_data.phone,
            email=contact_data.email,
            comment=contact_data.comment,
        )

        return await self.repository.create(contact)
