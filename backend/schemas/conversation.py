from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ConversationCreate(BaseModel):
    user_id: UUID
    title: str


class ConversationRead(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    created_at: datetime

    model_config = {"from_attributes": True}
