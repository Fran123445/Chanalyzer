import pymongo
from models.models import Board, Thread

class MongoAccess:

    def __init__(self, connection_string: str, database_name: str,
                 board_collection_name: str, thread_collection_name: str):
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[database_name]
        self.board_collection = self.db[board_collection_name]
        self.thread_collection = self.db[thread_collection_name]

    def insert_threads_from_board(self, board: Board):
        board_name = board.board_name

        for thread in board.threads:
            self.thread_collection.update_one(
                {"boardName": board_name, "threadNumber": thread.thread_number},
                {"$set": {"semanticEmbedding": list(thread.semantic_embedding)}},
                upsert=True)

    def insert_board(self, board: Board):
        self.board_collection.update_one(
            {"boardName": board.board_name},
            {"$set": {"semanticEmbedding": list(board.semantic_embedding)}},
            upsert=True)

        self.insert_threads_from_board(board)