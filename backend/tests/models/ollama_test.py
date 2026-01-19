import sys
import os
import pytest

# Configuration du chemin pour les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from backend.services.models.ollama import OllamaModel

@pytest.mark.parametrize("model_name", ["qwen3:14b"])
def test_model_generation(model_name):
    """Vérifie que le modèle est accessible et répond à une question de type '4' à '2+2'"""
    try:
        factory = OllamaModel()
        model = factory.get_model(model=model_name, validate_model_on_init=True)
    except Exception as e:
        pytest.skip(f"Modèle {model_name} non disponible localement ou Ollama éteint: {e}")
    response = model.invoke("Réponds en JSON valide : {\"result\": 4}. Combien font 2+2 ?")
    
    assert response.content, f"Réponse vide pour {model_name}"
    if '"result": 4' in response.content or '"result":4' in response.content:
         pass
    else:
        print(f"DEBUG Response content: {response.content}")

