from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MessageCreate(BaseModel):
    conversation_id: UUID
    role: str
    content: str


class MessageRead(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
