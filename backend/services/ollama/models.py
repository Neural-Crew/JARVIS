# https://reference.langchain.com/python/integrations/langchain_ollama/#langchain_ollama.ChatOllama
# https://docs.langchain.com/oss/python/integrations/chat/ollama
from langchain_ollama import ChatOllama # pyright: ignore[reportMissingImports]

# https://ollama.com/library/qwen3
qwen3_14b = ChatOllama(
    model="qwen3:14b",
    reasoning=False
)
