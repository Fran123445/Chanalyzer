import numpy as np

from services.embedders.embedder import Embedder
from sentence_transformers import SentenceTransformer
from services.utils.aggregator import Aggregator

class SemanticEmbedder(Embedder):

        def __init__(self, model: SentenceTransformer, aggregator: Aggregator):
            self.model = model
            self.aggregator = aggregator

        def embed_text(self, text: str):
            embedding = self.model.encode(text, convert_to_numpy=True)

            return embedding.astype(np.float64)

        def embed_text_list(self, text_list: list[str], weights_list: list[int]):
            """Generates the embedding of a list of texts by averaging the embeddings of the individual texts."""
            embeddings = self.model.encode(text_list, convert_to_numpy=True)

            average_embedding = self.aggregator.get_average_embedding(embeddings, weights_list)

            return average_embedding.astype(np.float64)
