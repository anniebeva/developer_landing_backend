import logging

from openai import AsyncOpenAI
import json

from app.core.config import settings
from app.ai.prompts import SYSTEM_PROMPT
from app.schemas.analysis import AIAnalysisResult

logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    api_key=settings.AI_API_KEY,
    base_url=settings.AI_BASE_URL,
)


async def analyze_contact(comment: str) -> AIAnalysisResult | None:
    """Analyze contact request using AI model."""

    if not settings.AI_API_KEY:
        return None

    try:
        response = await client.chat.completions.create(
            model=settings.AI_MODEL,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": comment,
                },
            ],
        )

        data = json.loads(response.choices[0].message.content)

        result = AIAnalysisResult(**data, source="ai")

        logger.info(
            "AI analysis completed: sentiment=%s priority=%s",
            result.sentiment,
            result.priority,
        )

        return result

    except Exception:
        logger.exception("AI analysis failed")
        return None
