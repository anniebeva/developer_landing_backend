from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.models.contact import ContactRequest
from app.models.contact_analysis import ContactAnalysis

router = APIRouter(tags=["metrics"])


@router.get("/metrics")
async def get_metrics(session: AsyncSession = Depends(get_session)):
    """Return contact requests analytics."""

    total_result = await session.execute(select(func.count(ContactRequest.id)))
    total_contacts = total_result.scalar() or 0

    sentiment_result = await session.execute(
        select(
            ContactAnalysis.sentiment,
            func.count(ContactAnalysis.id),
        ).group_by(ContactAnalysis.sentiment)
    )

    sentiment = dict(sentiment_result.all())

    source_result = await session.execute(
        select(
            ContactAnalysis.source,
            func.count(ContactAnalysis.id),
        ).group_by(ContactAnalysis.source)
    )

    source = dict(source_result.all())

    priority_result = await session.execute(
        select(
            ContactAnalysis.priority,
            func.count(ContactAnalysis.id),
        ).group_by(ContactAnalysis.priority)
    )

    priority = dict(priority_result.all())

    return {
        "total_contacts": total_contacts,
        "sentiment": {
            "positive": sentiment.get("positive", 0),
            "neutral": sentiment.get("neutral", 0),
            "negative": sentiment.get("negative", 0),
        },
        "analysis_source": {
            "ai": source.get("ai", 0),
            "fallback": source.get("fallback", 0),
        },
        "priority": {
            "high": priority.get("high", 0),
            "medium": priority.get("medium", 0),
            "low": priority.get("low", 0),
        },
    }
