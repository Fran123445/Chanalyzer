from typing import Optional

from models.thread import Thread

class Board:

    def __init__(self, board_name: str,
                 threads: Optional[list[Thread]] = None,
                 semantic_embedding: Optional[tuple[float]] = None):

        self.board_name = board_name
        self.threads = threads
        self.semantic_embedding = semantic_embedding
