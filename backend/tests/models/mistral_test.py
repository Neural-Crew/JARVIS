import sys
import os
import pytest
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from backend.services.models.mistral import MistralModel

load_dotenv()

@pytest.mark.parametrize("model_name", ["mistral-tiny"])
def test_mistral_generation(model_name):
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        pytest.skip("MISTRAL_API_KEY manquante")

    model = MistralModel().get_model(model=model_name, api_key=api_key)
    response = model.invoke("Combien font 2+2 ? Réponds juste avec le chiffre")
    
    assert response.content
    assert "4" in str(response.content)

if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))