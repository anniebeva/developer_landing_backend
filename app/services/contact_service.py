from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import ContactRepository
from app.schemas import ContactCreate


class ContactService:
    def __init__(self, session: AsyncSession):
        self.repository = ContactRepository(session)

    async def create_contact(self, contact_data: ContactCreate):
        contact = await self.repository.create(contact_data)

        return contact
