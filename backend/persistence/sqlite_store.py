from __future__ import annotations

from datetime import datetime, timezone
from backend.utils.singleton import Singleton
from backend.persistence.Model.ecowatch_bd import Conversation, Message
from backend.persistence.engine import engine
from sqlalchemy import select, insert

def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class SQLiteChatStore(metaclass=Singleton):
    """Minimal SQLite storage for chat conversations and messages."""

    def get_or_create_conversation_id(self, session_id: str) -> int :
        with engine.begin() as conn:
            stmt = select(Conversation.id).where(Conversation.session_id==session_id)
            row = conn.execute(stmt).first()
            if row:
                return int(row[0])
            stmt = insert(Conversation).values(session_id=session_id, created_at=_utc_now_iso() )
            cur = conn.execute(stmt)
            return int(cur.lastrowid)

    def get_messages(self, session_id: str) -> list[dict]:
        conversation_id = self.get_or_create_conversation_id(session_id)
        with engine.begin() as conn:
            stmt = select(Message).where(Message.conversation_id==conversation_id).order_by(Message.id.asc())
            rows = conn.execute(stmt)
                        
            return [
                {
                    "role": row.role,
                    "content": row.content,
                    "timestamp": row.timestamp,
                }
                for row in rows
            ]

    def add_message(self, q_session_id: str, q_role: str, q_content: str) -> None:
        conversation_id = self.get_or_create_conversation_id(q_session_id)
        with engine.begin() as conn:
            stmt = insert(Message).values(conversation_id=conversation_id, role=q_role, content=q_content, timestamp=_utc_now_iso() )
            conn.execute(stmt)
