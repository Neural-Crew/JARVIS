import json

import pytest
from fastapi.testclient import TestClient

import backend.main as main_module
from backend.persistence.sqlite_store import SQLiteChatStore


@pytest.fixture
def chat_store(tmp_path, monkeypatch):
    store = SQLiteChatStore(db_path=str(tmp_path / "chat_api.db"))
    monkeypatch.setattr(main_module, "store", store)
    return store


@pytest.fixture
def client(chat_store):
    with TestClient(main_module.app) as test_client:
        yield test_client


def _extract_streamed_tokens(raw_ndjson: str) -> str:
    tokens: list[str] = []
    for line in raw_ndjson.splitlines():
        line = line.strip()
        if not line:
            continue
        payload = json.loads(line)
        if payload.get("type") == "token":
            tokens.append(payload.get("content", ""))
    return "".join(tokens)


def testGivenBlankMessageWhenPostChatThenReturns400(client):
    response = client.post("/chat", json={"session_id": "session-a", "message": "   "})

    assert response.status_code == 400
    assert response.json()["detail"] == "message cannot be empty"


def testGivenBlankSessionIdWhenPostChatThenReturns400(client):
    response = client.post("/chat", json={"session_id": "   ", "message": "hello"})

    assert response.status_code == 400
    assert response.json()["detail"] == "session_id cannot be empty"


def testGivenChatRequestWhenStreamingThenSavesUserAndAssistantMessages(
    client, chat_store, monkeypatch
):
    async def fake_stream_chat(history, on_token=None):
        assert history[-1]["role"] == "user"
        assert history[-1]["content"] == "Bonjour"
        for token in ["Salut", " !"]:
            if on_token is not None:
                on_token(token)
            yield json.dumps({"type": "token", "content": token}) + "\n"

    monkeypatch.setattr(main_module, "stream_chat", fake_stream_chat)

    response = client.post("/chat", json={"session_id": "session-save", "message": "Bonjour"})

    assert response.status_code == 200
    assert _extract_streamed_tokens(response.text) == "Salut !"

    history = chat_store.get_messages("session-save")
    assert [m["role"] for m in history] == ["user", "assistant"]
    assert history[0]["content"] == "Bonjour"
    assert history[1]["content"] == "Salut !"


def testGivenUnknownSessionWhenGetMessagesThenReturnsEmptyList(client):
    response = client.get("/chat/new-session/messages")

    assert response.status_code == 200
    assert response.json() == []


def testGivenExistingSessionWhenGetMessagesThenReturnsOrderedHistory(client, chat_store):
    chat_store.add_message(session_id="session-history", role="user", content="Question")
    chat_store.add_message(session_id="session-history", role="assistant", content="Reponse")

    response = client.get("/chat/session-history/messages")

    assert response.status_code == 200
    payload = response.json()
    assert [item["role"] for item in payload] == ["user", "assistant"]
    assert [item["content"] for item in payload] == ["Question", "Reponse"]


def testGivenTwoSessionIdsWhenStoreMessagesThenHistoriesAreIsolated(chat_store):
    chat_store.add_message(session_id="session-one", role="user", content="A")
    chat_store.add_message(session_id="session-two", role="user", content="B")

    history_one = chat_store.get_messages("session-one")
    history_two = chat_store.get_messages("session-two")

    assert [m["content"] for m in history_one] == ["A"]
    assert [m["content"] for m in history_two] == ["B"]

