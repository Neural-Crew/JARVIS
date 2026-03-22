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
from backend.tools.ecowatch_sensors import (get_all_sensor_data,
                                            get_latest_sensor_data,
                                            get_sensor_history,
                                            list_ecowatch_devices,
                                            test_ecowatch_connection)

load_dotenv()

_agent = None


def _get_agent():
    global _agent
    if _agent is None:
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise RuntimeError("MISTRAL_API_KEY is required to use /chat")
        model = MistralModel().get_model(api_key=api_key, temperature=0)
        #model = OllamaModel().get_model(temperature=0)
        _agent = create_agent(model=model, tools=[
            test_ecowatch_connection,
            get_latest_sensor_data,
            list_ecowatch_devices,
            get_sensor_history,
            get_all_sensor_data
        ])
    return _agent


async def stream_chat(history: list[dict]):
    """
    Gère la conversation, transforme l'historique brut en messages LangChain, invoque l'agent et stream la réponse token par token.

    Args:
        history (list[dict]): Liste des messages au format `{"role": "user"|"assistant", "content": "..."}`.

    Yields:
        str: Les fragments de texte générés par le modèle (tokens).
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
    async for event in agent.astream_events({"messages": lc_messages}, version="v2"):
        event_type = event.get("event")
        data = event.get("data", {})

        if event_type == "on_chat_model_stream":
            chunk = data.get("chunk")
            if chunk and chunk.content:
                yield ToolNdjson()._to_ndjson_line({"type": "token", "content": chunk.content})
        else: yield ToolNdjson.handleEvent(event_type, event, data)
