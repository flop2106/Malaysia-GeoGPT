#Create Embedding Call To API
#Subscribe From scraper topic reingest to kafka with additional embedding

from LLM.BaseLLM import BaseLLM
from Kafka.KafkaConsumer import consume_topics
from Kafka.KafkaPublisher import publish
from Database.SqlLiteSetup import PaperTable,EmbeddingsTable
import json
import utils.LoggerBaseUtil as LoggerBaseUtil
logger = LoggerBaseUtil.setup()

class Embedding(BaseLLM):
    def __init__(self):
        super().__init__()
        self.api_url = "https://api.openai.com/v1/embeddings"
        self.model = "text-embedding-3-small"
        PaperTable.initialize_table()
        EmbeddingsTable.initialize_table
    
    def execute(self, input: str):

        request_body = {
            "model": self.model,
            "input": input.replace("\n", " "),
        }

        response = self.post_request(self.api_url, request_body)

        return response['data'][0]['embedding']
    
    def embedding_sequence(self):

        list_of_reports = consume_topics(["scraper"],"scraper-group")
        print(x for x in list_of_reports)
        for message in list_of_reports:
            logger.info(f"This is the result: {message.topic} | {message.key}: {message.value}")
            #data = json.loads(message.value)
            data = message.value
            logger.info(f"Process For {data['title']}")
            logger.info("Inserting into SQLLite")
            PaperTable.insert_paper(data['title'],
                                        data['authors'],
                                        data['url'],
                                        data['abstract']
                                        
                                        )
            # get the paper_id from the database
            paper_id = PaperTable.get_paper_id()
            logger.info(f"Get paper id: {paper_id}")
            # perform embedding
            logger.info("Execute Embedding")
            embedding_result = self.execute(f"""
                        'Title': {data["title"]},
                        'Authors': {data["authors"]},
                        'Abstract': {data["abstract"]}
                         """)
            logger.info("Save Embedding in SQLLite")
            import numpy as np
            EmbeddingsTable.insert_embeddings(paper_id, np.array(embedding_result))
            logger.info("Completed!")                


if __name__ == "__main__":
    test = Embedding()
    print(test.execute("Hello Vector!"))
        