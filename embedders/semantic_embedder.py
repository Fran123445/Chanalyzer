from embedders.embedder import Embedder
from sentence_transformers import SentenceTransformer
import numpy as np
from models.models import Thread, Board

class SemanticEmbedder(Embedder):

        def __init__(self, model: SentenceTransformer):
            self.model = model

        def _get_weights(self, embeddings: np.array):
            n = embeddings.shape[0]
            positions = np.arange(1, n + 1)
            weights = 1 / positions

            return weights

        def _get_average_embedding(self, embeddings: np.array):
            weights = self._get_weights(embeddings)
            average_embedding = np.average(embeddings, axis=0, weights=weights)

            return average_embedding

        def embed(self, text: str):
            embedding = self.model.encode(text)

            return embedding

        def embed(self, text_list: list[str]):
            """Generates the embedding of a list of texts by averaging the embeddings of the individual texts."""
            embeddings = self.model.encode(text_list)

            average_embedding = self._get_average_embedding(embeddings)

            return average_embedding

        def calculate_thread_embedding(self, thread: Thread):
            thread_posts = thread.posts
            title = thread.thread_title

            # I know it's technically not a post but still
            if title is not None:
                thread_posts.insert(0, title)

            thread_embedding = self.embed(thread_posts)

            thread.semantic_embedding = thread_embedding

        def calculate_board_embedding(self, board: Board):
            thread_embeddings = []

            for thread in board.threads:
                if thread.semantic_embedding is None:
                    self.calculate_thread_embedding(thread)

                thread_embeddings.append(thread.semantic_embedding)

            board_embedding = self._get_average_embedding(np.array(thread_embeddings))

            board.semantic_embedding = board_embedding
