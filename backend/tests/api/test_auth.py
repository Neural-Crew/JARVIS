from __future__ import annotations

import os
import sys
import uuid
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

# Ensure imports that read env vars at module import time can initialize in tests.
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret-key")
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/test_db")

import backend.auth as auth_module
import backend.main as main_module
import backend.routes_auth as routes_auth_module
from backend.auth import get_current_user
from backend.db.database import get_db
from backend.main import app
from backend.security import verify_password


@pytest.fixture
def api_state(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    users_by_email: dict[str, SimpleNamespace] = {}
    users_by_id: dict[uuid.UUID, SimpleNamespace] = {}
    conversations: dict[uuid.UUID, SimpleNamespace] = {}
    messages: list[dict[str, Any]] = []

    fake_db = object()

    def fake_get_db():
        yield fake_db

    app.dependency_overrides[get_db] = fake_get_db

    def fake_get_user_by_email(_db: object, email: str) -> SimpleNamespace | None:
        return users_by_email.get(email)

    def fake_create_user(_db: object, *, email: str, password_hash: str) -> SimpleNamespace:
        user = SimpleNamespace(
            id=uuid.uuid4(),
            email=email,
            password_hash=password_hash,
            created_at=datetime.now(UTC),
        )
        users_by_email[email] = user
        users_by_id[user.id] = user
        return user

    def fake_get_user_by_id(_db: object, user_id: uuid.UUID) -> SimpleNamespace | None:
        return users_by_id.get(user_id)

    def fake_get_conversation_by_id(_db: object, conversation_id: uuid.UUID) -> SimpleNamespace | None:
        return conversations.get(conversation_id)

    def fake_create_conversation(_db: object, *, user_id: uuid.UUID, title: str) -> SimpleNamespace:
        conversation = SimpleNamespace(id=uuid.uuid4(), user_id=user_id, title=title)
        conversations[conversation.id] = conversation
        return conversation

    def fake_create_message(_db: object, *, conversation_id: uuid.UUID, role: str, content: str) -> None:
        messages.append(
            {
                "conversation_id": conversation_id,
                "role": role,
                "content": content,
            }
        )

    async def fake_stream_chat(_messages: list[dict[str, str]]):
        yield '{"type":"token","content":"Hello"}\n'

    monkeypatch.setattr(routes_auth_module, "get_user_by_email", fake_get_user_by_email)
    monkeypatch.setattr(routes_auth_module, "create_user", fake_create_user)
    monkeypatch.setattr(auth_module, "get_user_by_id", fake_get_user_by_id)

    monkeypatch.setattr(main_module, "get_user_by_id", fake_get_user_by_id)
    monkeypatch.setattr(main_module, "get_conversation_by_id", fake_get_conversation_by_id)
    monkeypatch.setattr(main_module, "create_conversation", fake_create_conversation)
    monkeypatch.setattr(main_module, "create_message", fake_create_message)
    monkeypatch.setattr(main_module, "stream_chat", fake_stream_chat)

    with TestClient(app) as client:
        yield {
            "client": client,
            "users_by_email": users_by_email,
            "users_by_id": users_by_id,
            "messages": messages,
        }

    app.dependency_overrides.clear()


def test_register_hashes_password_and_returns_user(api_state: dict[str, Any]) -> None:
    client = api_state["client"]

    response = client.post(
        "/auth/register",
        json={"email": "alice@example.com", "password": "StrongPass123!"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["email"] == "alice@example.com"

    stored_user = api_state["users_by_email"]["alice@example.com"]
    assert stored_user.password_hash != "StrongPass123!"
    assert verify_password("StrongPass123!", stored_user.password_hash)


def test_register_duplicate_email_returns_409(api_state: dict[str, Any]) -> None:
    client = api_state["client"]
    body = {"email": "alice@example.com", "password": "StrongPass123!"}

    first = client.post("/auth/register", json=body)
    second = client.post("/auth/register", json=body)

    assert first.status_code == 201
    assert second.status_code == 409


def test_login_returns_jwt_token(api_state: dict[str, Any]) -> None:
    client = api_state["client"]

    client.post(
        "/auth/register",
        json={"email": "alice@example.com", "password": "StrongPass123!"},
    )
    response = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "password": "StrongPass123!"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["access_token"], str)
    assert payload["token_type"] == "bearer"
    assert payload["expires_in"] == 7 * 24 * 60 * 60


def test_login_bad_password_returns_401(api_state: dict[str, Any]) -> None:
    client = api_state["client"]

    client.post(
        "/auth/register",
        json={"email": "alice@example.com", "password": "StrongPass123!"},
    )
    response = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401


def test_me_with_valid_token_returns_current_user(api_state: dict[str, Any]) -> None:
    client = api_state["client"]

    client.post(
        "/auth/register",
        json={"email": "alice@example.com", "password": "StrongPass123!"},
    )
    login_response = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "password": "StrongPass123!"},
    )
    token = login_response.json()["access_token"]

    me_response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert me_response.status_code == 200
    assert me_response.json()["email"] == "alice@example.com"


def test_me_with_invalid_token_returns_401(api_state: dict[str, Any]) -> None:
    client = api_state["client"]

    response = client.get("/auth/me", headers={"Authorization": "Bearer invalid.token.value"})

    assert response.status_code == 401


def test_chat_without_token_returns_401(api_state: dict[str, Any]) -> None:
    client = api_state["client"]

    response = client.post(
        "/chat",
        json={
            "user_id": str(uuid.uuid4()),
            "messages": [{"role": "user", "content": "Hi"}],
        },
    )

    assert response.status_code == 401


def test_chat_with_mismatched_user_returns_403(api_state: dict[str, Any]) -> None:
    client = api_state["client"]
    token_user = SimpleNamespace(id=uuid.uuid4())

    app.dependency_overrides[get_current_user] = lambda: token_user
    try:
        response = client.post(
            "/chat",
            headers={"Authorization": "Bearer any-token"},
            json={
                "user_id": str(uuid.uuid4()),
                "messages": [{"role": "user", "content": "Hi"}],
            },
        )
    finally:
        app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 403


def test_chat_with_valid_auth_streams_response(api_state: dict[str, Any]) -> None:
    client = api_state["client"]

    register_response = client.post(
        "/auth/register",
        json={"email": "alice@example.com", "password": "StrongPass123!"},
    )
    user_id = register_response.json()["id"]

    login_response = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "password": "StrongPass123!"},
    )
    token = login_response.json()["access_token"]

    response = client.post(
        "/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "user_id": user_id,
            "messages": [{"role": "user", "content": "Hi"}],
        },
    )

    assert response.status_code == 200
    assert '"type": "conversation"' in response.text
    assert '"type":"token"' in response.text
