from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contact import ContactRequest
from app.schemas.contact import ContactCreate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, contact_data: ContactCreate) -> ContactRequest:

        contact = ContactRequest(**contact_data.model_dump())

        self.session.add(contact)

        await self.session.commit()

        await self.session.refresh(contact)

        return contact
