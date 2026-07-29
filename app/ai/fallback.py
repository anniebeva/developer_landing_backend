from app.schemas.analysis import AIAnalysisResult

import logging

logger = logging.getLogger(__name__)


class FallbackAnalyzer:
    """Analyze contact requests without external AI."""

    def analyze(self, comment: str) -> AIAnalysisResult:
        """Analyze request using keyword matching."""

        text = comment.lower()

        sentiment = self._detect_sentiment(text)
        priority = self._detect_priority(text)

        logger.info("Fallback analysis used")

        return AIAnalysisResult(
            sentiment=sentiment,
            priority=priority,
            summary="Analysis generated using keyword rules.",
            source="fallback",
        )

    def _detect_sentiment(self, text: str) -> str:
        """Detect sentiment from keywords."""

        positive_words = [
            "спасибо",
            "отлично",
            "нравится",
            "хочу",
            "интересно",
        ]

        negative_words = [
            "плохо",
            "проблема",
            "ошибка",
            "не работает",
            "срочно",
        ]

        if any(word in text for word in positive_words):
            return "positive"

        if any(word in text for word in negative_words):
            return "negative"

        return "neutral"

    def _detect_priority(self, text: str) -> str:
        """Detect priority from urgency keywords."""

        high_priority_words = [
            "срочно",
            "как можно скорее",
            "горит",
            "немедленно",
            "urgent",
        ]

        low_priority_words = [
            "когда будет возможность",
            "не срочно",
            "просто узнать",
        ]

        if any(word in text for word in high_priority_words):
            return "high"

        if any(word in text for word in low_priority_words):
            return "low"

        return "medium"
