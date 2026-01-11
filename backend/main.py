from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Literal

from langchain_core.messages import HumanMessage, AIMessage
from backend.agent.agent import agent  # Reutilise l'agent existant

app = FastAPI()

# Format des messages echanges entre frontend et backend
class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

# Requete envoyee par le frontend (liste complete de messages)
class ChatRequest(BaseModel):
    messages: List[ChatMessage]

# Reponse renvoyee au frontend (dernier message de l'IA)
class ChatResponse(BaseModel):
    reply: str

@app.get("/")
def root():
    # Ping simple pour verifier que le serveur tourne
    return {"status": "ok", "service": "jarvis"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    # Evite une erreur 404 quand le navigateur demande l'icone
    return Response(status_code=204)

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # Convertit les messages en objets LangChain
    history = []
    for m in req.messages:
        if m.role == "user":
            history.append(HumanMessage(content=m.content))
        else:
            history.append(AIMessage(content=m.content))
    # Appel de l'agent avec tout l'historique
    result = agent.invoke({"messages": history})
    # On renvoie uniquement la derniere reponse de l'IA
    reply = result["messages"][-1].content
    return {"reply": reply}
