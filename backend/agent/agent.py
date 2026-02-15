import json
import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage

from backend.services.models.mistral import MistralModel
from backend.services.models.ollama import OllamaModel
from backend.tools.ecowatch_sensors import (
    get_all_sensor_data, get_latest_sensor_data, 
    get_sensor_history, list_ecowatch_devices, test_ecowatch_connection
)

load_dotenv()

# Instanciation simplifiée des modèles
MODELS = {
    "mistral": lambda: MistralModel().get_model(api_key=os.getenv("MISTRAL_API_KEY"), temperature=0),
    "ollama": lambda: OllamaModel().get_model(temperature=0),
}
agent = create_agent(model=MODELS["mistral"](), tools=[
    test_ecowatch_connection, get_latest_sensor_data, 
    list_ecowatch_devices, get_sensor_history, get_all_sensor_data
])

def _get_val(data: dict, keys: list) -> str:
    """Helper concis pour extraire la première valeur non-nulle d'une liste de clés"""
    for k in keys:
        if v := data.get(k): return str(v) if isinstance(v, (str, int, float)) else json.dumps(v, ensure_ascii=True)
    return ""

async def stream_chat(history: list[dict]):
    """
    Exécute l'agent et streame la réponse (tokens + événements outils) au format NDJSON.
    """
    # 1. Conversion de l'historique JSON -> Messages LangChain
    lc_messages = [
        HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
        for m in history
    ]

    try:
        # 2. Streaming des événements (version v2 de l'API astream_events)
        async for event in agent.astream_events({"messages": lc_messages}, version="v2"):
            kind, data = event["event"], event.get("data", {})
            payload = {}

            # Cas A : Streaming de texte (Token par token)
            if kind == "on_chat_model_stream" and (chunk := data.get("chunk")) and chunk.content:
                payload = {"type": "token", "content": chunk.content}
            
            # Cas B : Événements liés aux outils (Start -> End/Error)
            elif kind.startswith("on_tool_"):
                step = kind.replace("on_", "")
                # On ne garde que les événements pertinents pour le frontend
                if step not in ("start", "end", "error"): continue
                
                payload = {
                    "type": f"tool_{step}",
                    "run_id": event.get("run_id"),
                    "name": event.get("name") or data.get("tool") or "tool",
                }
                
                # Extraction spécifique selon l'étape
                if step == "start": payload["input"] = _get_val(data, ["input_str", "input", "inputs"])
                elif step == "end": payload["output"] = _get_val(data, ["output", "outputs"])
                elif step == "error": payload["error"] = _get_val(data, ["error"])

            if payload:
                yield json.dumps(payload, ensure_ascii=True) + "\n"

    # 3. Gestion globale des erreurs pour ne pas casser le stream HTTP
    except Exception as e:
        yield json.dumps({"type": "error", "content": f"Erreur interne de l'agent: {str(e)}"}, ensure_ascii=True) + "\n"