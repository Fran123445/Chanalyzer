from services.data_access.mongo.mongo_access import MongoAccess
from services.embedders.semantic_embedder import SemanticEmbedder
from services.matcher.matcher import Matcher


class BoardFinder:

    def __init__(self, mongo_access: MongoAccess,
                 semantic_embedder: SemanticEmbedder,
                 matcher: Matcher):
        self.mongo_access = mongo_access
        self.semantic_embedder = semantic_embedder
        self.matcher = matcher

    def find_similar_to_board(self, board_name: str, top_n: int):
        board = self.mongo_access.get_board(board_name)
        board_embedding = board.semantic_embedding

        top_similar_boards = self.matcher.get_top_similar_boards(board_embedding, "semantic_embedding", top_n)

        return top_similar_boards