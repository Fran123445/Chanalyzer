from embedders.embedder import Embedder
from sentence_transformers import SentenceTransformer
from utils.aggregator import Aggregator

class SemanticEmbedder(Embedder):

        def __init__(self, model: SentenceTransformer, aggregator: Aggregator):
            self.model = model
            self.aggregator = aggregator

        def embed(self, text: str):
            embedding = self.model.encode(text)

            return embedding

        def embed(self, text_list: list[str]):
            """Generates the embedding of a list of texts by averaging the embeddings of the individual texts."""
            embeddings = self.model.encode(text_list)

            average_embedding = self.aggregator.get_average_embedding(embeddings)

            return average_embedding
