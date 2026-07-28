from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ContactAnalysis(Base):
    __tablename__ = "contact_analyses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    contact_request_id: Mapped[int] = mapped_column(
        ForeignKey("contact_requests.id"),
        nullable=False,
    )

    sentiment: Mapped[str] = mapped_column(String(50), nullable=False)

    priority: Mapped[str] = mapped_column(String(50), nullable=False)

    summary: Mapped[str] = mapped_column(Text, nullable=False)

    model: Mapped[str | None] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    contact_request = relationship("ContactRequest", back_populates="analysis")
