from abc import ABC, abstractmethod
from typing import Optional, Any, List, Dict, Union, Literal
from langchain_core.language_models import BaseChatModel

class ModelFactory(ABC):
    """Interface abstraite pour la création des modèles de langage (LLMs).

    Définit le contrat que toutes les factories de modèles doivent respecter.
    """
    
    @abstractmethod
    def get_model(
        self,
        model: str,
        temperature: float = 0.8,
        format: Optional[Union[Literal["", "json"], Dict[str, Any]]] = "json",
        **kwargs: Any
    ) -> BaseChatModel:
        """Crée et retourne une instance de modèle de chat configurée.

        Args:
            model: Le nom ou l'identifiant du modèle à charger.
            temperature: La température pour la génération (contrôle le déterminisme).
            format: Le format de sortie souhaité (ex: "json").
            **kwargs: Arguments supplémentaires spécifiques au fournisseur du modèle.

        Returns:
            Une instance configurée d'un modèle de chat LangChain.
        """
        pass

