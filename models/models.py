from dataclasses import dataclass
from typing import Optional


@dataclass
class Thread:
    thread_number: int
    posts: list[str]
    semantic_embedding: Optional[tuple[float]] = None

@dataclass
class Board:
    board_name: str
    threads: list[Thread]
    semantic_embedding: Optional[tuple[float]] = None

