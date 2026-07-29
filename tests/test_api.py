from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport

from app.main import app
from app.schemas.analysis import AIAnalysisResult
from app.core.rate_limit import requests_storage


@pytest_asyncio.fixture
async def client():
    """Create async test client."""

    requests_storage.clear()

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
def mock_external_services():
    """Mock external AI and email services."""

    with (
        patch(
            "app.services.contact_service.AIService.analyze_contact",
            new_callable=AsyncMock,
        ) as mock_ai,
        patch(
            "app.services.contact_service.EmailService.send_contact_notification",
            new_callable=AsyncMock,
        ) as mock_email,
    ):

        mock_ai.return_value = AIAnalysisResult(
            sentiment="positive",
            priority="medium",
            summary="Test AI analysis",
            source="ai",
        )

        mock_email.return_value = None

        yield


@pytest.mark.asyncio
async def test_health(client):
    """Check health endpoint."""

    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_metrics(client):
    """Check metrics endpoint."""

    response = await client.get("/metrics")

    assert response.status_code == 200

    data = response.json()

    assert "total_contacts" in data
    assert "sentiment" in data
    assert "analysis_source" in data
    assert "priority" in data


@pytest.mark.asyncio
async def test_create_contact(client, mock_external_services):
    """Create contact request successfully."""

    payload = {
        "name": "Test User",
        "phone": "+79999999999",
        "email": "test@example.com",
        "comment": "Спасибо, всё отлично",
    }

    response = await client.post(
        "/api/contact",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test User"
    assert data["phone"] == "+79999999999"
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_create_contact_invalid_email(client):
    """Reject contact with invalid email."""

    payload = {
        "name": "Test User",
        "phone": "+79999999999",
        "email": "wrong-email",
        "comment": "Hello",
    }

    response = await client.post(
        "/api/contact",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_contact_empty_name(client):
    """Reject contact without name."""

    payload = {
        "name": "",
        "phone": "+79999999999",
        "email": "test@example.com",
        "comment": "Hello",
    }

    response = await client.post(
        "/api/contact",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_rate_limit(client, mock_external_services):
    """Check spam protection."""

    payload = {
        "name": "Spam User",
        "phone": "+79999999999",
        "email": "spam@example.com",
        "comment": "test",
    }

    responses = []

    for _ in range(6):
        response = await client.post(
            "/api/contact",
            json=payload,
        )

        responses.append(response.status_code)

    assert 429 in responses


@pytest.mark.asyncio
async def test_ai_fallback(client):
    """Use fallback analysis when AI is unavailable."""

    with patch(
        "app.services.contact_service.AIService.analyze_contact",
        new_callable=AsyncMock,
    ) as mock_ai, patch(
        "app.services.contact_service.EmailService.send_contact_notification",
        new_callable=AsyncMock,
    ):

        mock_ai.return_value = AIAnalysisResult(
            sentiment="neutral",
            priority="medium",
            summary="Fallback analysis",
            source="fallback",
        )

        payload = {
            "name": "Fallback User",
            "phone": "+79999999999",
            "email": "fallback@example.com",
            "comment": "Спасибо, всё отлично",
        }

        response = await client.post("/api/contact", json=payload)

        assert response.status_code == 200
