from services.data_access.mongo.mongo_access import MongoAccess
from services.embedders.semantic_embedder import SemanticEmbedder
from services.matcher.matcher import Matcher

class BoardFinder:

    def __init__(self, mongo_access: MongoAccess,
                 embedder: SemanticEmbedder,
                 matcher: Matcher,
                 embedding_type: str):
        self.mongo_access = mongo_access
        self.embedder = embedder
        self.matcher = matcher
        self.embedding_type = embedding_type

    def find_similar_to_board(self, board_name: str, top_n: int):
        board = self.mongo_access.get_board(board_name)
        board_embedding = board.semantic_embedding

        top_similar_boards = self.matcher.get_top_similar_boards(board_embedding, self.embedding_type, top_n)
        top_similar_boards = top_similar_boards[1:]  # Remove the board itself from the list

        return top_similar_boards

    def find_similar_to_text(self, text: str, top_n: int):
        text_embedding = self.embedder.embed_text(text)

        top_similar_boards = self.matcher.get_top_similar_boards(text_embedding, self.embedding_type, top_n)

        return top_similar_boards

    def find_similar_to_text_list(self, text_list: list[str], weights_list: list[int], top_n: int):
        text_embedding = self.embedder.embed_text_list(text_list, weights_list)

        top_similar_boards = self.matcher.get_top_similar_boards(text_embedding, self.embedding_type, top_n)

        return top_similar_boards
