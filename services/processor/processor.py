from services.embedders.embedder import Embedder
from services.utils.aggregator import Aggregator
from models.models import Thread, Board
import numpy as np

class Processor:
    def __init__(self, embedder: Embedder, aggregator: Aggregator):
        self.embedder = embedder
        self.aggregator = aggregator

    def calculate_thread_embedding(self, thread: Thread):
        thread_posts = thread.posts
        title = thread.thread_title

        # I know it's technically not a post but still
        if title is not None:
            thread_posts.insert(0, title)

        thread_embedding = self.embedder.embed(thread_posts)

        thread.semantic_embedding = thread_embedding

    def calculate_board_embedding(self, board: Board):
        thread_embeddings = []

        for thread in board.threads:
            if thread.semantic_embedding is None:
                self.calculate_thread_embedding(thread)

            thread_embeddings.append(thread.semantic_embedding)

        board_embedding = self.aggregator.get_average_embedding(np.array(thread_embeddings))

        board.semantic_embedding = board_embedding