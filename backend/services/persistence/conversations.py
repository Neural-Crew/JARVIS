from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.db.models import Conversation


def get_conversation_by_id(db: Session, conversation_id: UUID) -> Conversation | None:
    stmt = select(Conversation).where(Conversation.id == conversation_id)
    return db.scalar(stmt)


def list_user_conversations(db: Session, user_id: UUID) -> list[Conversation]:
    stmt = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
    )
    return list(db.scalars(stmt).all())


def create_conversation(db: Session, *, user_id: UUID, title: str) -> Conversation:
    conversation = Conversation(user_id=user_id, title=title)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation
