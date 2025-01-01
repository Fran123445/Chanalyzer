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