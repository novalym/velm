import os
from openai import OpenAI
from ....contracts.heresy_contracts import ArtisanHeresy


class NeuralEncoder:
    """[THE ENCODER] Transmutes Text into Floating Point Vectors."""

    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def embed(self, text_list: list[str], model: str) -> list[list[float]]:
        try:
            # Replace newlines to improve performance
            clean_texts = [t.replace("\n", " ") for t in text_list]
            response = self.client.embeddings.create(input=clean_texts, model=model)
            return [data.embedding for data in response.data]
        except Exception as e:
            raise ArtisanHeresy(f"Embedding Fracture: {e}")