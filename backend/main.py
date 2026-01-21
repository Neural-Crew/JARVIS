from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from typing import List, AsyncGenerator

from backend.agent.agent import stream_chat

app = FastAPI()

@app.post("/chat")
async def chat_endpoint(request: dict = Body(...)):
    """
    Accepte un JSON brut: {"messages": [{"role": "...", "content": "..."}]}
    Renvoie la réponse de l'IA en chunks via HTTP Streaming.
    """
    messages = request.get("messages", [])
    return StreamingResponse(
        stream_chat(messages), # La méthode streamchat vient de agent.py
        media_type="text/plain"
    )

@app.get("/")
def root():
    """HealthCheck"""
    return {"status": "ok", "service": "jarvis"}

