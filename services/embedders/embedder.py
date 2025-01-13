from abc import ABC, abstractmethod

class Embedder(ABC):

    @abstractmethod
    def embed_text(self, text: str):
        pass

    @abstractmethod
    def embed_text_list(self, text_list: list[str],  weights_list: list[int]):
        pass