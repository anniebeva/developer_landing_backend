from app.core.exceptions import ContactCreationError


class ContactRepository:

    def __init__(self, session):
        self.session = session

    async def create(self, contact):
        try:
            self.session.add(contact)

            await self.session.commit()
            await self.session.refresh(contact)

            return contact

        except Exception as exc:
            await self.session.rollback()
            raise ContactCreationError() from exc
