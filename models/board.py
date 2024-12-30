from dataclasses import dataclass
from typing import Optional

from models.thread import Thread

@dataclass
class Board:
    board_name: str
    threads: Optional[list[Thread]] = None
    semantic_embedding: Optional[tuple[float]] = None
