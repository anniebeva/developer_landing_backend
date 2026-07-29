from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class ContactCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=5, max_length=30)
    email: EmailStr
    comment: str = Field(min_length=5, max_length=2000)

    @field_validator("name", "comment")
    @classmethod
    def strip_text(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str):
        value = value.strip()

        if not value.replace("+", "").replace("-", "").isdigit():
            raise ValueError("Invalid phone format")

        return value


class ContactResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True
