from embedders.embedder import Embedder
from sentence_transformers import SentenceTransformer

class SemanticEmbedder(Embedder):

        def __init__(self, model: SentenceTransformer):
            self.model = model

        def embed(self, text):
            embeddings = self.model.encode(text)

            return embeddings

