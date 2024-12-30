from typing import Optional

class Thread:

    def __init__(self, board: str,
                 thread_number: int,
                 thread_title: Optional[str] = None,
                 posts: Optional[list[str]] = None,
                 semantic_embedding: Optional[tuple[float]] = None):

        self.board = board
        self.thread_number = thread_number
        self.thread_title = thread_title
        self.posts = posts
        self.semantic_embedding = semantic_embedding
