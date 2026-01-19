import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from frontend.app import iter_chat_stream


class FakeResponse:
    def __init__(self, chunks, status_code=200):
        self._chunks = chunks
        self.status_code = status_code

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def iter_content(self, chunk_size=None, decode_unicode=True):
        for chunk in self._chunks:
            yield chunk


class FakeRequests:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def post(self, url, json, stream=True):
        self.calls.append({"url": url, "json": json, "stream": stream})
        return self.response


def test_iter_chat_stream_yields_chunks():
    response = FakeResponse(["Hello", " ", "world"])
    fake_requests = FakeRequests(response)
    messages = [{"role": "user", "content": "hi"}]

    output = "".join(iter_chat_stream(messages, api_url="http://api", requests_module=fake_requests))

    assert output == "Hello world"
    assert fake_requests.calls == [
        {"url": "http://api", "json": {"messages": messages}, "stream": True}
    ]


def test_iter_chat_stream_skips_empty_chunks():
    response = FakeResponse(["a", "", None, "b"])
    fake_requests = FakeRequests(response)

    output = "".join(iter_chat_stream([], api_url="http://api", requests_module=fake_requests))

    assert output == "ab"
