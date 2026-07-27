from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class ContactCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=5, max_length=30)
    email: EmailStr
    comment: str = Field(min_length=5, max_length=2000)


class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True
