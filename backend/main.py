import json
from collections.abc import AsyncGenerator

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.agent.agent import stream_chat
from backend.auth import get_current_user
from backend.db.database import get_db
from backend.db.models import User
from backend.routes_auth import router as auth_router
from backend.schemas.chat import ChatRequest
from backend.services.persistence.conversations import (create_conversation,
                                                        get_conversation_by_id)
from backend.services.persistence.messages import create_message
from backend.services.persistence.users import get_user_by_id

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)


def _build_title(request: ChatRequest) -> str:
    if request.title:
        return request.title[:255]

    for message in request.messages:
        if message.role == "user":
            return message.content[:255]
    return "New conversation"


def _extract_last_user_message(request: ChatRequest) -> str:
    for message in reversed(request.messages):
        if message.role == "user":
            return message.content
    raise HTTPException(status_code=422, detail="At least one user message is required.")


@app.post("/chat")
async def chat_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Accepts JSON: {"user_id": "...", "messages": [{"role": "...", "content": "..."}]}
    Streams AI chunks over HTTP and persists conversation messages.
    """
    if request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot access another user's conversations.")

    user_content = _extract_last_user_message(request)
    user = get_user_by_id(db, request.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    if request.conversation_id is not None:
        conversation = get_conversation_by_id(db, request.conversation_id)
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found.")
        if conversation.user_id != request.user_id:
            raise HTTPException(status_code=403, detail="Conversation does not belong to user.")
    else:
        conversation = create_conversation(
            db,
            user_id=request.user_id,
            title=_build_title(request),
        )

    create_message(
        db,
        conversation_id=conversation.id,
        role="user",
        content=user_content,
    )

    async def _stream_and_persist() -> AsyncGenerator[str, None]:
        assistant_chunks: list[str] = []
        yield json.dumps({"type": "conversation", "conversation_id": str(conversation.id)}) + "\n"

        async for line in stream_chat([message.model_dump() for message in request.messages]):
            if line:
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    payload = None

                if isinstance(payload, dict) and payload.get("type") == "token":
                    content = payload.get("content")
                    if isinstance(content, str):
                        assistant_chunks.append(content)

                yield line

        assistant_content = "".join(assistant_chunks).strip()
        if assistant_content:
            create_message(
                db,
                conversation_id=conversation.id,
                role="assistant",
                content=assistant_content,
            )

    return StreamingResponse(
        _stream_and_persist(),
        media_type="application/x-ndjson",
    )


@app.get("/")
def root():
    """HealthCheck"""
    return {"status": "ok", "service": "jarvis"}
