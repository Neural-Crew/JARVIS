import sys
import os

from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from backend.main import app
import backend.main as main_module


def test_root_healthcheck():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "jarvis"}


def test_chat_streaming(monkeypatch):
    received = {}

    async def fake_stream_chat(messages):
        received["messages"] = messages
        for chunk in ["hello", " ", "world"]:
            yield chunk

    monkeypatch.setattr(main_module, "stream_chat", fake_stream_chat)

    client = TestClient(app)
    response = client.post("/chat", json={"messages": [{"role": "user", "content": "hi"}]})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert response.text == "hello world"
    assert received["messages"] == [{"role": "user", "content": "hi"}]


def test_chat_streaming_defaults_to_empty_messages(monkeypatch):
    received = {}

    async def fake_stream_chat(messages):
        received["messages"] = messages
        if False:
            yield ""

    monkeypatch.setattr(main_module, "stream_chat", fake_stream_chat)

    client = TestClient(app)
    response = client.post("/chat", json={})

    assert response.status_code == 200
    assert received["messages"] == []
