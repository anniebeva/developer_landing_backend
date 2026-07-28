from datetime import datetime

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ContactRequest(Base):
    """Database model for incoming contact requests."""

    __tablename__ = "contact_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    phone: Mapped[str] = mapped_column(String(30), nullable=False)

    email: Mapped[str] = mapped_column(String(255), nullable=False)

    comment: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    analysis = relationship(
        "ContactAnalysis",
        back_populates="contact_request",
        uselist=False,
        cascade="all, delete-orphan",
    )
