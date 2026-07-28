from app.core.config import settings
from app.ai.client import analyze_contact
from app.ai.fallback import FallbackAnalyzer


class AIService:
    """Service for analyzing contact requests."""

    def __init__(self):
        self.fallback = FallbackAnalyzer()

    async def analyze_contact(self, comment: str):
        """Analyze contact request using AI or fallback."""

        if not settings.AI_API_KEY:
            return self.fallback.analyze(comment)

        try:
            result = await analyze_contact(comment)

            if result:
                return result

        except Exception as exc:
            print(f"AI analysis failed: {exc}")

        return self.fallback.analyze(comment)
