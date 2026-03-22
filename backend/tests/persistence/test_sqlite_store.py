import sqlite3

import pytest

from backend.persistence.sqlite_store import SQLiteChatStore


def testGivenFreshStoreWhenInitializeThenCreatesRequiredTables(tmp_path):
    db_path = tmp_path / "chat_store.db"
    SQLiteChatStore(db_path=str(db_path))

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    table_names = {row[0] for row in rows}

    assert "conversations" in table_names
    assert "messages" in table_names


def testGivenSessionIdWhenGetOrCreateTwiceThenReturnsSameConversationId(tmp_path):
    store = SQLiteChatStore(db_path=str(tmp_path / "chat_store.db"))

    first = store.get_or_create_conversation_id("session-a")
    second = store.get_or_create_conversation_id("session-a")

    assert first == second


def testGivenMessagesWhenStoreAndReadThenKeepsChronologicalOrder(tmp_path):
    store = SQLiteChatStore(db_path=str(tmp_path / "chat_store.db"))
    session_id = "session-order"

    store.add_message(session_id=session_id, role="user", content="Bonjour")
    store.add_message(session_id=session_id, role="assistant", content="Salut")
    store.add_message(session_id=session_id, role="user", content="Suite")

    history = store.get_messages(session_id)

    assert [m["role"] for m in history] == ["user", "assistant", "user"]
    assert [m["content"] for m in history] == ["Bonjour", "Salut", "Suite"]


def testGivenInvalidRoleWhenAddMessageThenRaisesIntegrityError(tmp_path):
    store = SQLiteChatStore(db_path=str(tmp_path / "chat_store.db"))

    with pytest.raises(sqlite3.IntegrityError):
        store.add_message(session_id="session-invalid", role="system", content="x")

