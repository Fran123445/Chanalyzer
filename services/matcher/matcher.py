import sentence_transformers.util

from services.data_access.mongo.mongo_access import MongoAccess

class Matcher:

    def __init__(self, mongo_access: MongoAccess):
        self.mongo_access = mongo_access

    def calculate_similarities(self, embedding: list, element_list: list, embedding_type: str):
        similarity_dict = {}

        for element in element_list:
            similarity_tensor = sentence_transformers.util.cos_sim(embedding, getattr(element, embedding_type))
            similarity_dict[element] = similarity_tensor.item()

        return similarity_dict

    def get_top_similar_boards(self, embedding: list, embedding_type: str, top_n: int):
        boards = self.mongo_access.get_boards()

        similarity_dict = self.calculate_similarities(embedding, boards, embedding_type)

        top_similar_boards = sorted(similarity_dict.items(), key=lambda x: x[1], reverse=True)[:top_n]
        top_similar_boards = [(board.board_name, similarity) for board, similarity in top_similar_boards]

        return top_similar_boards