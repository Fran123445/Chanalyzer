import pyodbc
from fastapi import FastAPI
from contextlib import asynccontextmanager

from sentence_transformers import SentenceTransformer

from config import *
from services.board_finder.board_finder import BoardFinder
from services.data_access.mongo.mongo_access import MongoAccess
from services.data_access.sql.sql_access import SQLAccess
from services.embedders.semantic_embedder import SemanticEmbedder
from services.matcher.matcher import Matcher
from services.processor.processor import Processor
from services.utils.aggregator import Aggregator

@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = pyodbc.connect(f"Driver={SQL_DB_DRIVER};"
                                f"Server={SQL_DB_SERVER};"
                                f"Database={SQL_DB_NAME};"
                                "Trusted_connection=yes;")

    sql_access = SQLAccess(connection)
    mongo_access = MongoAccess(MONGO_DB_SERVER,MONGO_DB_NAME, MONGO_COLLECTION_BOARDS, MONGO_COLLECTION_THREADS)

    transformer = SentenceTransformer(TRANSFORMER_MODEL_NAME)
    aggregator = Aggregator()
    embedder = SemanticEmbedder(transformer, aggregator)
    matcher = Matcher(mongo_access)
    board_finder = BoardFinder(mongo_access, embedder, matcher, "semantic_embedding")

    app.state.semantic_processor = Processor(embedder, aggregator, sql_access, mongo_access)
    app.state.sql_access = sql_access
    app.state.mongo_access = mongo_access
    app.state.board_finder = board_finder

    yield

    app.state.sql_access.close_connection()
    app.state.mongo_access.close_connection()


app = FastAPI(title="Chanalyzer API", lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Welcome to the Chanalyzer API"}