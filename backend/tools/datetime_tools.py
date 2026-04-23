from datetime import datetime

from langchain_core.tools import tool


@tool(parse_docstring=True)
def get_current_datetime() -> dict:
    """Retourne la date et l'heure actuelles du serveur.

    Cette fonction est utile pour répondre aux questions relatives à la date et l'heure courantes.

    Returns:
        Dictionnaire contenant la date et l'heure au format ISO 8601 local.
    """
    now_local = datetime.now().astimezone()

    return {
        "datetime_local": now_local.isoformat(),
    }
