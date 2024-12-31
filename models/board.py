from typing import Optional

import numpy as np

from models.thread import Thread

class Board:

    def __init__(self, board_name: str,
                 threads: Optional[list[Thread]] = None,
                 semantic_embedding: Optional[np.ndarray] = None):

        self.board_name = board_name
        self.threads = threads
        self.semantic_embedding = semantic_embedding

    def __hash__(self):
        return hash(self.board_name)

    def __eq__(self, other):
        return self.board_name == other.board_name
