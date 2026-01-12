import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage

from backend.services.models.mistral import MistralModel
from backend.services.models.ollama import OllamaModel
from backend.tools.ecowatch import get_environmental_data

load_dotenv()

# Instantation du modèle et de l'agent
model = MistralModel().get_model(api_key=os.getenv("MISTRAL_API_KEY"), temperature=0)
#model = OllamaModel().get_model(temperature=0)
agent = create_agent(model=model, tools=[get_environmental_data])


async def stream_chat(history: list[dict]):
    """
    Gère la conversation, transforme l'historique brut en messages LangChain, invoque l'agent et stream la réponse token par token.

    Args:
        history (list[dict]): Liste des messages au format `{"role": "user"|"assistant", "content": "..."}`.

    Yields:
        str: Les fragments de texte générés par le modèle (tokens).
    """
    lc_messages = [
        HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
        for m in history
    ]
    async for event in agent.astream_events({"messages": lc_messages}, version="v2"):
        if event["event"] == "on_chat_model_stream":
            chunk = event["data"].get("chunk")
            if chunk and chunk.content:
                yield chunk.content

        
        
