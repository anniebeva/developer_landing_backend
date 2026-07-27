from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Developer Landing Backend"

    DATABASE_URL: str

    AI_API_KEY: str | None = None
    AI_BASE_URL: str | None = None
    AI_MODEL: str | None = None

    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    OWNER_EMAIL: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
