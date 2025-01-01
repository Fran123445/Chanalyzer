import pymongo
from models.board import Board
from models.thread import Thread
import numpy as np


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

    def get_board(self, board_name: str):
        board = self.board_collection.find_one({"boardName": board_name})

        return Board(board_name=board["boardName"], semantic_embedding=np.array(board["semanticEmbedding"]))

    def get_boards(self):
        cursor = self.board_collection.find()
        boards = []

        for board in cursor:
            board_name = board["boardName"]
            semantic_embedding = np.array(board["semanticEmbedding"])
            # If I didn't explicitly cast it here, it would be converted to an array of Python floats,
            # which would cause a crash when doing similarity comparison as Pytorch
            # converts floats to float32 instead of float64

            boards.append(Board(board_name=board_name, semantic_embedding=semantic_embedding))

        return boards

    def close_connection(self):
        self.client.close()