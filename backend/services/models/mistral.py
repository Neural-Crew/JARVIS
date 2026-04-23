"""Implémentation du modèle Mistral AI.

Ce module permet d'instancier des modèles ChatMistralAI configurés avec
des paramètres optimisés (streaming, rate limiting, format JSON).
"""

from typing import Optional, Any, Dict, Union, Literal, List
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from .models import ModelFactory

load_dotenv()

class MistralModel(ModelFactory):
    """Factory pour les modèles de langage Mistral AI.
    """

    def get_model(
        self,
        model: str = "mistral-large-latest",
        temperature: float = 0.8,
        format: Optional[Union[Literal["", "json"], Dict[str, Any]]] = "json",
        max_retries: int = 5,
        top_p: float = 1.0,
        disable_streaming: bool = False,
        api_key: Optional[str] = None,
        **kwargs: Any
    ) -> ChatMistralAI:
        """Configure et retourne une instance de ChatMistralAI.

        Args:
            model: Identifiant du modèle (ex: "mistral-large-latest").
            temperature: Température de génération.
            format: Format de sortie (ex: "json").
            max_retries: Nombre d'essais en cas d'échec.
            top_p: Nucleus sampling.
            disable_streaming: Désactive le streaming si vrai.
            api_key: Clé API Mistral (utilise l'environnement si None).
            **kwargs: Autres paramètres passés au constructeur.

        Returns:
            Une instance configurée de ChatMistralAI.
        """
        model_kwargs = kwargs.pop("model_kwargs", {})
        return ChatMistralAI(
            model=model, # type: ignore
            temperature=temperature,
            max_retries=max_retries,
            top_p=top_p,
            disable_streaming=disable_streaming,
            api_key=api_key,
            model_kwargs=model_kwargs,
            **kwargs
        )
