import sentence_transformers.util

from services.data_access.mongo.mongo_access import MongoAccess

class Matcher:

    def __init__(self, mongo_access: MongoAccess):
        self.mongo_access = mongo_access

    def calculate_similarities(self, embedding: list, embedding_type: str):
        boards = self.mongo_access.get_boards()

        similarity_dict = {}

        for board in boards:
            similarity = sentence_transformers.util.cos_sim(embedding, getattr(board, embedding_type))
            similarity_dict[board.name] = similarity

        return similarity_dict

    def get_top_similar_boards(self, embedding: list, embedding_type: str, top_n: int):
        similarity_dict = self.calculate_similarities(embedding, embedding_type)

        top_similar_boards = sorted(similarity_dict.items(), key=lambda x: x[1], reverse=True)[:top_n]

        return top_similar_boards