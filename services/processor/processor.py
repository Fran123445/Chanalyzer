from services.data_access.mongo.mongo_access import MongoAccess
from services.data_access.sql.sql_access import SQLAccess
from services.embedders.embedder import Embedder
from services.utils.aggregator import Aggregator
from models.board import Board
from models.thread import Thread
from config import *
import numpy as np

class Processor:
    def __init__(self, embedder: Embedder, aggregator: Aggregator,
                sql_access: SQLAccess, mongo_access: MongoAccess):
        self.embedder = embedder
        self.aggregator = aggregator
        self.sql_access = sql_access
        self.mongo_access = mongo_access

    def calculate_thread_embedding(self, thread: Thread):
        thread_posts = thread.posts
        title = thread.thread_title

        # I know it's technically not a post but still
        if title is not None:
            thread_posts.insert(0, title)

        thread_embedding = self.embedder.embed_text_list(thread_posts)

        thread.semantic_embedding = thread_embedding

    def calculate_board_embedding(self, board: Board):
        thread_embeddings = []

        for thread in board.threads:
            if thread.semantic_embedding is None:
                self.calculate_thread_embedding(thread)

            thread_embeddings.append(thread.semantic_embedding)

        board_embedding = self.aggregator.get_average_embedding(np.array(thread_embeddings))

        board.semantic_embedding = board_embedding

    def process_board(self, board_name: str):
        board =self.sql_access.get_board_with_threads(board_name, THREAD_AMOUNT, POST_AMOUNT, MIN_WORDS_PER_POST)
        self.calculate_board_embedding(board)
        self.mongo_access.insert_board(board)