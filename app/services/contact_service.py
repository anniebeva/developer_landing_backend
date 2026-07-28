from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

from app.models.contact import ContactRequest
from app.models.contact_analysis import ContactAnalysis
from app.repositories import (
    ContactRepository,
    ContactAnalysisRepository,
)
from app.schemas import ContactCreate
from app.services.ai_service import AIService


class ContactService:
    """Business logic for contact requests."""

    def __init__(self, session: AsyncSession):
        self.repository = ContactRepository(session)
        self.analysis_repository = ContactAnalysisRepository(session)
        self.ai_service = AIService()

    async def create_contact(
        self,
        contact_data: ContactCreate,
    ):
        """Create contact request and save AI analysis."""

        analysis = await self.ai_service.analyze_contact(
            contact_data.comment,
        )

        contact = ContactRequest(
            name=contact_data.name,
            phone=contact_data.phone,
            email=contact_data.email,
            comment=contact_data.comment,
        )

        contact = await self.repository.create(contact)

        contact_analysis = ContactAnalysis(
            contact_request_id=contact.id,
            sentiment=analysis.sentiment,
            priority=analysis.priority,
            summary=analysis.summary,
            source=analysis.source,
            model=(settings.AI_MODEL if analysis.source == "ai" else None),
        )

        await self.analysis_repository.create(
            contact_analysis,
        )

        return contact
