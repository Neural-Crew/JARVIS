from typing import Optional, Any, List, Dict, Union, Literal
from langchain_ollama import ChatOllama
from .models import ModelFactory

class OllamaModel(ModelFactory):
    """Implémentation de la factory pour les modèles hébergés localement via Ollama.
    """

    def get_model(
        self,
        model: str = "qwen3:14b",
        temperature: float = 0.8,
        format: Optional[Union[Literal["", "json"], Dict[str, Any]]] = "",
        keep_alive: Optional[Union[str, int]] = None,
        num_ctx: Optional[int] = None,
        num_predict: Optional[int] = None,
        seed: Optional[int] = None,
        stop: Optional[List[str]] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        disable_streaming: bool = False,
        validate_model_on_init: bool = False,
        reasoning: bool = False,
        **kwargs: Any
    ) -> ChatOllama:
        """Configure et retourne un modèle Ollama.

        Args:
            model: Le nom du modèle local (ex: "qwen3:14b", "llama3").
            temperature: La température pour la génération.
            format: Le format de sortie (ex: "json").
            keep_alive: Durée de maintien du modèle en mémoire.
            num_ctx: Taille de la fenêtre de contexte.
            num_predict: Nombre maximum de tokens à générer.
            seed: Graine aléatoire pour la reproductibilité.
            stop: Séquences d'arrêt pour la génération.
            top_k: Limite le vocabulaire aux K tokens les plus probables.
            top_p: Nucleus sampling.
            disable_streaming: Désactive le streaming si vrai.
            validate_model_on_init: Vérifie l'existence du modèle au démarrage.
            reasoning: Active les capacités de raisonnement si supporté.
            **kwargs: Autres paramètres passés à ChatOllama.

        Returns:
            Une instance configurée de ChatOllama.
        """
        
        return ChatOllama(
            model=model,
            temperature=temperature,
            format=format,
            keep_alive=keep_alive,
            num_ctx=num_ctx,
            num_predict=num_predict,
            seed=seed,
            stop=stop,
            top_k=top_k,
            top_p=top_p,
            disable_streaming=disable_streaming,
            validate_model_on_init=validate_model_on_init,
            reasoning=reasoning,
            **kwargs
        )
