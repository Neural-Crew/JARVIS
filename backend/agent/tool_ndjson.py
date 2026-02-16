import json

class ToolNdjson:
    @staticmethod
    def handleEvent( event_type, event, data ) -> str:
        ndjson = ToolNdjson()
        run_id = event.get("run_id")
        match event_type:
            case "on_tool_start":
                return ndjson._to_ndjson_line(
                {
                    "type": "tool_start",
                    "run_id": run_id,
                    "name": ndjson._tool_name(event),
                    "input": ndjson._tool_input(data),
                })
                
            case "on_tool_end":
                return ndjson._to_ndjson_line(
                {
                    "type": "tool_end",
                    "run_id": run_id,
                    "name": ndjson._tool_name(event),
                    "output": ndjson._tool_output(data),
                }
            )
            
            case "on_tool_error":
                return ndjson._to_ndjson_line(
                {
                    "type": "tool_error",
                    "run_id": run_id,
                    "name": ndjson._tool_name(event),
                    "error": ndjson._tool_error(data),
                }
            )
            case _:
                return ""

    def _to_ndjson_line(self, payload: dict) -> str:
        return f"{json.dumps(payload, ensure_ascii=True)}\n"
    
    def _tool_name(self, event: dict) -> str:
        name = event.get("name")
        if name:
            return name
        data = event.get("data", {})
        serialized = data.get("serialized", {})
        return serialized.get("name") or data.get("tool") or "tool"
    
    def _tool_input(self, data: dict) -> str:
        if "input_str" in data and data["input_str"] is not None:
            return str(data["input_str"])
        if "input" in data and data["input"] is not None:
            return str(data["input"])
        if "inputs" in data and data["inputs"] is not None:
            return json.dumps(data["inputs"], ensure_ascii=True)
        return ""


    def _tool_output(self, data: dict) -> str:
        if "output" in data and data["output"] is not None:
            return str(data["output"])
        if "outputs" in data and data["outputs"] is not None:
            return json.dumps(data["outputs"], ensure_ascii=True)
        return ""


    def _tool_error(self, data: dict) -> str:
        if "error" in data and data["error"] is not None:
            return str(data["error"])
        return ""