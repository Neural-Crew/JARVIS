import sys
import os
import pytest

# Configuration du chemin pour les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import backend.services.ollama.models as ollama_models
from backend.config.test import MODELS_TO_TEST

@pytest.mark.parametrize("var_name", MODELS_TO_TEST)
def test_model_generation(var_name):
    """Vérifie que le modèle est accessible et répond '4' à '2+2'"""
    # Récupération du modèle
    model = getattr(ollama_models, var_name, None)
    assert model is not None, f"Modèle {var_name} introuvable dans models.py"
    
    # Invocation réelle
    response = model.invoke("Combien font 2+2 ? Réponds juste par le chiffre.")
    
    # Vérification
    assert "4" in response.content, f"Échec pour {var_name}: réponse '{response.content}'"

if __name__ == "__main__":
    sys.exit(pytest.main([ __file__]))
