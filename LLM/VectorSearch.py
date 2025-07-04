from LLM.BaseLLM import BaseLLM
from LLM.Embedding import Embedding
from Database.SqlLiteSetup import get_all

import utils.LoggerBaseUtil as LoggerBaseUtil

import struct
import math

logger = LoggerBaseUtil.setup()

def _blob_to_floats(blob: bytes)-> list:
    """Convert BLOB data from SQLite into a list of floats"""
    if not blob:
        return []
    count = len(blob)//8
    return list(struct.unpack(f"{count}d", blob))

def _cosine_similarity(a: list, b: list) -> float:
    """
    Return cosine similarity between two vectors.
    """

    dot = sum(x*y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

class VectorSearch(BaseLLM):
    def __init__(self):
        super().__init__()

    def vector_search(self, query_embedding: list, embeddings_table: list,
                      top_k: int = 50) -> list:
        """
        Compute cosine similarity and return top_k paper id
        """
        scores = []
        for row in embeddings_table:
            _, embedding_blob, paper_id = row
            embedding_vec = _blob_to_floats(embedding_blob)
            if not embedding_vec:
                continue
            sim = _cosine_similarity(query_embedding, embedding_vec)
            scores.append((sim, paper_id))
        scores.sort(key = lambda x: x[0], reverse = True)
        return [paper_id for _, paper_id in scores[:top_k]]

    def execute(self, query:str) -> list:
        #query all embeddings from database
        embeddings_table = get_all("embeddings")
        # convert query to embeddings
        embedding = Embedding()
        query_embeddings = embedding.execute(query)
        list_of_top_paper_id = self.vector_search(query_embeddings, 
                                                     embeddings_table)
        #get all rows from listpaper table with list_of_top_10_paper_id
        if not list_of_top_paper_id:
            return []
        condition = f" paper_id in ({','.join(map(str, list_of_top_paper_id))})"
        listpaper_table = get_all("listpaper", condition)

        return listpaper_table
