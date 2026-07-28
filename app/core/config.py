from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    APP_NAME: str = "Developer Landing Backend"

    DATABASE_URL: str

    # AI provider configuration
    AI_API_KEY: str | None = None
    AI_BASE_URL: str = "https://openrouter.ai/api/v1"
    AI_MODEL: str = "google/gemini-2.0-flash-exp:free"

    # Email configuration
    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    OWNER_EMAIL: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
