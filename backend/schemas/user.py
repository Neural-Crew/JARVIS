from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password_hash: str


class UserRead(BaseModel):
    id: UUID
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}
