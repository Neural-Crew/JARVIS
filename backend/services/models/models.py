from abc import ABC, abstractmethod
from typing import Optional, Any, List, Dict, Union, Literal
from langchain_core.language_models import BaseChatModel

class ModelFactory(ABC): # (ABC) => définis les règles d'héritage
    """
    Interface abstraite pour la création des modèles LLMs
    """
    
    @abstractmethod
    def get_model(
        self,
        model: str,
        temperature: float = 0.8,
        format: Optional[Union[Literal["", "json"], Dict[str, Any]]] = "json",
        **kwargs: Any
    ) -> BaseChatModel:
        """
        Crée et retourne une instance de modèle de chat configurée.
        """
        pass

