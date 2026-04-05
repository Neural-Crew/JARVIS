from datetime import datetime

from langchain_core.tools import tool


@tool(parse_docstring=True)
def get_current_datetime() -> dict:
    """Retourne la date et l'heure actuelles du serveur.

    Utilisez ce tool quand l'utilisateur demande:
    - La date actuelle
    - L'heure actuelle
    - Le jour actuel
    - Le timestamp courant

    Returns:
        Dictionnaire contenant uniquement `datetime_local`.
    """
    now_local = datetime.now().astimezone()

    return {
        "datetime_local": now_local.isoformat(),
    }
