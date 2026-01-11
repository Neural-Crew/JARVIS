from typing import Optional, Any, List, Dict, Union, Literal
from langchain_ollama import ChatOllama
from .models import ModelFactory

class OllamaModel(ModelFactory):
    def get_model(
        self,
        model: str = "qwen3:14b",
        temperature: float = 0.8,
        format: Optional[Union[Literal["", "json"], Dict[str, Any]]] = "json",
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
