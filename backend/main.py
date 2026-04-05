from typing import AsyncGenerator, List

from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from backend.agent.agent import stream_chat

app = FastAPI()

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
async def chat_endpoint(request: dict = Body(...)):
    """
    Accepte un JSON brut: {"messages": [{"role": "...", "content": "..."}]}
    Renvoie la réponse de l'IA en chunks via HTTP Streaming.
    """
    messages = request.get("messages", [])
    return StreamingResponse(
        stream_chat(messages), # La méthode streamchat vient de agent.py
        media_type="application/x-ndjson",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache",
        },
    )

@app.get("/")
def root():
    """HealthCheck"""
    return {"status": "ok", "service": "jarvis"}

