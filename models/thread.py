from dataclasses import dataclass
from typing import Optional


@dataclass
class Thread:
    board: str
    thread_number: int
    thread_title: Optional[str] = None
    posts: Optional[list[str]] = None
    semantic_embedding: Optional[tuple[float]] = None
