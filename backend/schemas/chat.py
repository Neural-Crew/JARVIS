from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(pattern="^(user|assistant|system)$")
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    user_id: UUID
    messages: list[ChatMessage]
    conversation_id: UUID | None = None
    title: str | None = None
