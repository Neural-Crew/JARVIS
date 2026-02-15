import json
import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage

from backend.services.models.mistral import MistralModel
from backend.services.models.ollama import OllamaModel
from backend.tools.ecowatch_sensors import (get_all_sensor_data,
                                            get_latest_sensor_data,
                                            get_sensor_history,
                                            list_ecowatch_devices,
                                            test_ecowatch_connection)

load_dotenv()

# Instantation du modèle et de l'agent
model = MistralModel().get_model(api_key=os.getenv("MISTRAL_API_KEY"), temperature=0)
#model = OllamaModel().get_model(temperature=0)
agent = create_agent(model=model, tools=[
    test_ecowatch_connection,
    get_latest_sensor_data,
    list_ecowatch_devices,
    get_sensor_history,
    get_all_sensor_data
])


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
        event_type = event.get("event")
        data = event.get("data", {})
        run_id = event.get("run_id")
        if event_type == "on_chat_model_stream":
            chunk = data.get("chunk")
            if chunk and chunk.content:
                yield _to_ndjson_line({"type": "token", "content": chunk.content})
        elif event_type == "on_tool_start":
            yield _to_ndjson_line(
                {
                    "type": "tool_start",
                    "run_id": run_id,
                    "name": _tool_name(event),
                    "input": _tool_input(data),
                }
            )
        elif event_type == "on_tool_end":
            yield _to_ndjson_line(
                {
                    "type": "tool_end",
                    "run_id": run_id,
                    "name": _tool_name(event),
                    "output": _tool_output(data),
                }
            )
        elif event_type == "on_tool_error":
            yield _to_ndjson_line(
                {
                    "type": "tool_error",
                    "run_id": run_id,
                    "name": _tool_name(event),
                    "error": _tool_error(data),
                }
            )


def _to_ndjson_line(payload: dict) -> str:
    return f"{json.dumps(payload, ensure_ascii=True)}\n"


def _tool_name(event: dict) -> str:
    name = event.get("name")
    if name:
        return name
    data = event.get("data", {})
    serialized = data.get("serialized", {})
    return serialized.get("name") or data.get("tool") or "tool"


def _tool_input(data: dict) -> str:
    if "input_str" in data and data["input_str"] is not None:
        return str(data["input_str"])
    if "input" in data and data["input"] is not None:
        return str(data["input"])
    if "inputs" in data and data["inputs"] is not None:
        return json.dumps(data["inputs"], ensure_ascii=True)
    return ""


def _tool_output(data: dict) -> str:
    if "output" in data and data["output"] is not None:
        return str(data["output"])
    if "outputs" in data and data["outputs"] is not None:
        return json.dumps(data["outputs"], ensure_ascii=True)
    return ""


def _tool_error(data: dict) -> str:
    if "error" in data and data["error"] is not None:
        return str(data["error"])
    return ""

        
        
