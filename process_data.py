import pyodbc
from sentence_transformers import SentenceTransformer

from services.data_access.mongo.mongo_access import MongoAccess
from services.data_access.sql.sql_access import SQLAccess
from services.embedders.semantic_embedder import SemanticEmbedder
from services.processor.processor import Processor
from services.utils.aggregator import Aggregator
from config import *

# Entry point for (eventually) running this and BoardCrawler using airflow

connection = pyodbc.connect(f"Driver={SQL_DB_DRIVER};"
                                f"Server={SQL_DB_SERVER};"
                                f"Database={SQL_DB_NAME};"
                                "Trusted_connection=yes;")
sql_access = SQLAccess(connection)
mongo_access = MongoAccess(MONGO_DB_SERVER,MONGO_DB_NAME, MONGO_COLLECTION_BOARDS, MONGO_COLLECTION_THREADS)

transformer = SentenceTransformer(TRANSFORMER_MODEL_NAME)

aggregator = Aggregator()
embedder = SemanticEmbedder(transformer, aggregator)
processor = Processor(embedder, aggregator)

boards = sql_access.get_boards()

for board_tuple in boards:
    board_name = board_tuple[0]

    # Again, I'm not dealing with /f/ for now (or never, who knows)
    if board_name == 'f':
        continue

    board = sql_access.get_board_with_threads(board_name, 150, 50, 4)

    processor.calculate_board_embedding(board)

    mongo_access.insert_board(board)