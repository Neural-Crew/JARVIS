from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator
from backend.utils.singleton import Singleton

def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class SQLiteChatStore(metaclass=Singleton):
    """Minimal SQLite storage for chat conversations and messages."""

    def __init__(self, db_path: str = "chat.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY(conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id)"
            )

    def get_or_create_conversation_id(self, session_id: str) -> int:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id FROM conversations WHERE session_id = ?",
                (session_id,),
            ).fetchone()
            if row:
                return int(row["id"])

            cur = conn.execute(
                "INSERT INTO conversations (session_id, created_at) VALUES (?, ?)",
                (session_id, _utc_now_iso()),
            )
            return int(cur.lastrowid)

    def get_messages(self, session_id: str) -> list[dict]:
        conversation_id = self.get_or_create_conversation_id(session_id)
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT role, content, timestamp
                FROM messages
                WHERE conversation_id = ?
                ORDER BY id ASC
                """,
                (conversation_id,),
            ).fetchall()
            return [
                {
                    "role": row["role"],
                    "content": row["content"],
                    "timestamp": row["timestamp"],
                }
                for row in rows
            ]

    def add_message(self, session_id: str, role: str, content: str) -> None:
        conversation_id = self.get_or_create_conversation_id(session_id)
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO messages (conversation_id, role, content, timestamp)
                VALUES (?, ?, ?, ?)
                """,
                (conversation_id, role, content, _utc_now_iso()),
            )
