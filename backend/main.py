from typing import AsyncGenerator, List

from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from backend.agent.agent import stream_chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
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
    try:
        messages = request.get("messages", [])
        if not messages:
             return {"error": "No messages provided"}, 400
             
        return StreamingResponse(
            stream_chat(messages), 
            media_type="application/x-ndjson"
        )
    except Exception as e:
        return {"error": str(e)}, 500

@app.get("/")
def root():
    """HealthCheck"""
    return {"status": "ok", "service": "jarvis"}

