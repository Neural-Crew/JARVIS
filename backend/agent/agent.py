import json
import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from backend.agent.tool_ndjson import ToolNdjson
from backend.services.models.mistral import MistralModel
from backend.services.models.ollama import OllamaModel
from backend.services.models.rate_limiter import mistral_rate_limiter
from backend.tools.datetime_tools import get_current_datetime
from backend.tools.ecowatch_sensors import (generate_sensor_chart,
                                            get_latest_sensor_data,
                                            get_sensor_history,
                                            list_ecowatch_devices,
                                            test_ecowatch_connection)

load_dotenv()

_agent = None


def _get_agent() -> "CompiledStateGraph":
    """Initialise et retourne l'agent LangChain.

    Configure le modèle Mistral avec la clé API et les outils nécessaires.

    Returns:
        L'agent LangChain (graphe LangGraph) prêt à l'emploi.

    Raises:
        RuntimeError: Si la variable d'environnement MISTRAL_API_KEY n'est pas définie.
    """
    global _agent
    if _agent is None:
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise RuntimeError("MISTRAL_API_KEY is required to use /chat")
        model = MistralModel().get_model(
            api_key=api_key, temperature=0, rate_limiter=mistral_rate_limiter
        )
        #model = OllamaModel().get_model(temperature=0)
        _agent = create_agent(model=model, tools=[
            get_current_datetime,
            test_ecowatch_connection,
            get_latest_sensor_data,
            list_ecowatch_devices,
            get_sensor_history,
            generate_sensor_chart,
        ])
    return _agent


from typing import AsyncGenerator


async def stream_chat(history: list[dict]) -> AsyncGenerator[str, None]:
    """Gère la conversation et stream la réponse de l'agent.

    Transforme l'historique brut en messages LangChain, invoque l'agent
    et renvoie la réponse token par token au format NDJSON.

    Args:
        history: Liste des messages de la conversation.

    Yields:
        Lignes au format NDJSON contenant les tokens ou les événements de l'agent.

    Raises:
        Exception: En cas d'erreur lors du chargement du prompt système ou du streaming.
    """

    # Charge le prompt système
    system_prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
    system_message = None
    try:
        with open(system_prompt_path, "r", encoding="utf-8") as f:
            system_message = SystemMessage(content=f.read())
    except Exception as e:
        print(f"Error loading system prompt: {e}")

    lc_messages = [
        HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
        for m in history
    ]

    if system_message:
        lc_messages.insert(0, system_message)

    agent = _get_agent()
    try:
        async for event in agent.astream_events({"messages": lc_messages}, version="v2"):
            event_type = event.get("event")
            data = event.get("data", {})

            if event_type == "on_chat_model_stream":
                chunk = data.get("chunk")
                if chunk and chunk.content:
                    yield ToolNdjson()._to_ndjson_line({"type": "token", "content": chunk.content})
            else:
                line = ToolNdjson.handleEvent(event_type, event, data)
                if line:
                    yield line
    except Exception as e:
        print(f"[stream_chat] Error during agent stream: {e}")
        yield ToolNdjson()._to_ndjson_line({
            "type": "token",
            "content": f"\n\n⚠️ Une erreur est survenue (rate limit ou réseau). Veuillez réessayer dans quelques secondes."
        })
