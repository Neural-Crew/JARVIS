import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from backend.agent.agent import stream_chat
from backend.persistence.Controller.sqlite_store import SQLiteChatStore

class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1)

class HistoryMessage(BaseModel):
    role: str
    content: str
    timestamp: str


def _default_db_path() -> str:
    # Keep DB at repository root by default: ./chat.db
    return str(Path(__file__).resolve().parents[1] / "chat.db")

app = FastAPI()
store = SQLiteChatStore()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.1.172:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_content = request.message.strip()
    if not user_content:
        raise HTTPException(status_code=400, detail="message cannot be empty")

    session_id = request.session_id.strip()
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id cannot be empty")

    history = store.get_messages(session_id)
    history_with_current = [*history, {"role": "user", "content": user_content}]

    # Persist user input before model call to keep consistent timeline.
    store.add_message(q_session_id=session_id, q_role="user", q_content=user_content)

    async def _stream_and_persist():
        assistant_chunks: list[str] = []

        def _collect(token: str) -> None:
            assistant_chunks.append(token)

        try:
            async for line in stream_chat(history_with_current, on_token=_collect):
                yield line
        finally:
            assistant_text = "".join(assistant_chunks).strip()
            if assistant_text:
                store.add_message(
                    q_session_id=session_id,
                    q_role="assistant",
                    q_content=assistant_text,
                )
    return StreamingResponse(
        _stream_and_persist(), # La méthode streamchat vient de agent.py
        media_type="application/x-ndjson",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache",
        },
    )


@app.get("/chat/{session_id}/messages", response_model=list[HistoryMessage])
async def get_session_messages(session_id: str):
    normalized = session_id.strip()
    if not normalized:
        raise HTTPException(status_code=400, detail="session_id cannot be empty")
    return store.get_messages(normalized)

# async def chat_endpoint(request: dict = Body(...)):
#     """
#     Accepte un JSON brut: {"messages": [{"role": "...", "content": "..."}]}
#     Renvoie la réponse de l'IA en chunks via HTTP Streaming.
#     """
#     messages = request.get("messages", [])
#     return StreamingResponse(
#         stream_chat(messages), # La méthode streamchat vient de agent.py
#         media_type="application/x-ndjson",
#         headers={
#             "X-Accel-Buffering": "no",
#             "Cache-Control": "no-cache",
#         },
#     )

@app.get("/")
def root():
    """HealthCheck"""
    return {"status": "ok", "service": "jarvis"}
