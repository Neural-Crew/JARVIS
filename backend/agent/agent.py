import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from backend.services.models.mistral import MistralModel
from backend.services.models.ollama import OllamaModel
load_dotenv()

# Instantation du modèle et de l'agent
#model = MistralModel().get_model(api_key=os.getenv("MISTRAL_API_KEY"), temperature=0)
model = OllamaModel().get_model(temperature=0)
agent = create_agent(model=model, tools=[])

if __name__ == "__main__":
    chat_history = []
    
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["q", "quit"]: break
        
        # On ajoute le message de l'utilisateur à l'historique
        chat_history.append(HumanMessage(content=user_input))     
        # On invoque l'agent avec l'historique actuel
        result = agent.invoke({"messages": chat_history})   
        # On récupère la réponse de l'IA (dernier message dans l'état retourné)
        last_message = result["messages"][-1]
        print(f"AI: {last_message.content}")
        
        
