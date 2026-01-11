from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Literal

from langchain_core.messages import HumanMessage, AIMessage
from backend.agent.agent import agent  # reuse existing agent

app = FastAPI()

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    reply: str

@app.get("/")
def root():
    return {"status": "ok", "service": "jarvis"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    history = []
    for m in req.messages:
        if m.role == "user":
            history.append(HumanMessage(content=m.content))
        else:
            history.append(AIMessage(content=m.content))
    result = agent.invoke({"messages": history})
    reply = result["messages"][-1].content
    return {"reply": reply}
