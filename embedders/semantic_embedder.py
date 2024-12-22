from embedders.embedder import Embedder
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticEmbedder(Embedder):

        def __init__(self, model: SentenceTransformer):
            self.model = model

        def _get_weights(self, embeddings: np.array):
            n = embeddings.shape[0]
            positions = np.arange(1, n + 1)
            weights = 1 / positions

            return weights

        def embed(self, text: str):
            embedding = self.model.encode(text)

            return embedding

        def embed(self, text_list: list[str]):
            """Generates the embedding of a list of texts by averaging the embeddings of the individual texts."""
            embeddings = self.model.encode(text_list)

            weights = self._get_weights(embeddings)
            average_embedding = np.average(embeddings, axis=0, weights=weights)

            return average_embedding
