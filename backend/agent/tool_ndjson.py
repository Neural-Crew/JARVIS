import json


class ToolNdjson:
    """Classe utilitaire pour la gestion des événements de l'agent au format NDJSON.

    Permet de transformer les événements LangChain en lignes JSON pour le streaming.
    """

    @staticmethod
    def handleEvent(event_type: str, event: dict, data: dict) -> str:
        """Gère un événement de l'agent et retourne une ligne NDJSON correspondante.

        Args:
            event_type: Le type d'événement reçu.
            event: Le dictionnaire complet de l'événement.
            data: Les données associées à l'événement.

        Returns:
            Une chaîne de caractères représentant l'événement au format NDJSON, ou une chaîne vide.
        """
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
        """Sérialise un dictionnaire en une ligne NDJSON.

        Args:
            payload: Le dictionnaire à sérialiser.

        Returns:
            La ligne JSON terminée par un saut de ligne.
        """
        return f"{json.dumps(payload, ensure_ascii=True)}\n"

    def _tool_name(self, event: dict) -> str:
        """Extrait le nom de l'outil à partir de l'événement.

        Args:
            event: L'événement de l'agent.

        Returns:
            Le nom de l'outil identifié.
        """
        name = event.get("name")
        if name:
            return name
        data = event.get("data", {})
        serialized = data.get("serialized", {})
        return serialized.get("name") or data.get("tool") or "tool"

    def _serialize_tool_value(self, value) -> str:
        """Sérialise une valeur d'outil (entrée ou sortie) en chaîne.

        Args:
            value: La valeur à sérialiser (dict, list ou autre).

        Returns:
            La représentation textuelle ou JSON de la valeur.
        """
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=True)
        return str(value)

    def _tool_input(self, data: dict) -> str:
        """Extrait et sérialise l'entrée d'un outil.

        Args:
            data: Les données de l'événement 'on_tool_start'.

        Returns:
            L'entrée de l'outil sous forme de chaîne.
        """
        if "input_str" in data and data["input_str"] is not None:
            return str(data["input_str"])
        if "input" in data and data["input"] is not None:
            input_value = data["input"]
            return self._serialize_tool_value(input_value)
        if "inputs" in data and data["inputs"] is not None:
            inputs_value = data["inputs"]
            return self._serialize_tool_value(inputs_value)
        return ""


    def _tool_output(self, data: dict) -> str:
        """Extrait et sérialise la sortie d'un outil.

        Args:
            data: Les données de l'événement 'on_tool_end'.

        Returns:
            La sortie de l'outil sous forme de chaîne.
        """
        if "output" in data and data["output"] is not None:
            output = data["output"]
            return self._serialize_tool_value(output)
        if "outputs" in data and data["outputs"] is not None:
            return json.dumps(data["outputs"], ensure_ascii=True)
        return ""


    def _tool_error(self, data: dict) -> str:
        """Extrait l'erreur d'un outil.

        Args:
            data: Les données de l'événement 'on_tool_error'.

        Returns:
            Le message d'erreur.
        """
        if "error" in data and data["error"] is not None:
            return str(data["error"])
        return ""