import aiosmtplib
from email.message import EmailMessage

from app.core.config import settings


class EmailService:
    """Service for sending email notifications."""

    async def send_contact_notification(
        self,
        name: str,
        email: str,
        phone: str,
        comment: str,
    ) -> None:
        """Send contact request notification to owner and user."""

        if not self._is_configured():
            return

        await self._send_email(
            recipient=settings.OWNER_EMAIL,
            subject="New contact request",
            body=self._build_owner_message(
                name=name,
                email=email,
                phone=phone,
                comment=comment,
            ),
        )

        await self._send_email(
            recipient=email,
            subject="Your request has been received",
            body=(
                "Thank you for contacting us.\n\n"
                "We have received your request and will reply soon."
            ),
        )

    async def _send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
    ) -> None:
        """Send email using configured SMTP server."""

        message = EmailMessage()

        message["From"] = settings.SMTP_USER
        message["To"] = recipient
        message["Subject"] = subject

        message.set_content(body)

        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )

    def _build_owner_message(
        self,
        name: str,
        email: str,
        phone: str,
        comment: str,
    ) -> str:
        """Build notification message for website owner."""

        return (
            "New contact request:\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n\n"
            "Comment:\n"
            f"{comment}"
        )

    def _is_configured(self) -> bool:
        """Check whether SMTP settings are configured."""

        return all(
            [
                settings.SMTP_HOST,
                settings.SMTP_PORT,
                settings.SMTP_USER,
                settings.SMTP_PASSWORD,
                settings.OWNER_EMAIL,
            ]
        )
