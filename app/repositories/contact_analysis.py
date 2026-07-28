from app.models.contact_analysis import ContactAnalysis


class ContactAnalysisRepository:
    """Repository for contact analysis database operations."""

    def __init__(self, session):
        self.session = session

    async def create(self, analysis: ContactAnalysis) -> ContactAnalysis:
        """Save contact analysis in database."""

        self.session.add(analysis)

        await self.session.commit()
        await self.session.refresh(analysis)

        return analysis
