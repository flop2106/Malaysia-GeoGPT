from LLM.BaseLLM import BaseLLM
from LLM.Embedding import Embedding
from Database.SqlLiteSetup import *

import utils.LoggerBaseUtil as LoggerBaseUtil

logger = LoggerBaseUtil.setup()

class VectorSearch(BaseLLM):
    def __init__(self):
        super().__init__()

    def vector_search(self):
        # return list of top_paper_id
        pass

    def execute(self, query:str) -> list:
        #query all from embeddings
        embeddings_table = get_all("embeddings")
        # convert query to embeddings
        query_embeddings = Embedding.execute(query)
        # perform vector search

        #return list of top 10 paper_id
        list_of_top_10_paper_id = self.vector_search()
        #get all rows from listpaper table with list_of_top_10_paper_id
        listpaper_table = get_all("listpaper",f"paper_id in ({','.join(list_of_top_10_paper_id)})")

        return listpaper_table
