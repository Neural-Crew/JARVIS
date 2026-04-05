from typing import Optional, Any, Dict, Union, Literal, List
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from .models import ModelFactory

load_dotenv()

class MistralModel(ModelFactory):
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
        """
        Implémentation de la factory pour Mistral AI.
        Référence: https://api.python.langchain.com/en/latest/chat_models/langchain_mistralai.chat_models.ChatMistralAI.html
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
