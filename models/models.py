from dataclasses import dataclass
from typing import Optional


@dataclass
class Thread:
    thread_number: int
    posts: list[str]
    embedding: Optional[tuple[float]] = None

@dataclass
class Board:
    board_name: str
    threads: list[Thread]
    embedding: Optional[tuple[float]] = None

