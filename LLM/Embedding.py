#Create Embedding Call To API
#Subscribe From scraper topic reingest to kafka with additional embedding

from LLM.BaseLLM import BaseLLM
from Kafka.KafkaConsumer import consume_topics
from Kafka.KafkaPublisher import publish
from Database.SqlLiteSetup import PaperTable,EmbeddingsTable
import json
import utils.LoggerBaseUtil as LoggerBaseUtil
import threading
import queue
logger = LoggerBaseUtil.setup()

class Embedding(BaseLLM):
    def __init__(self):
        super().__init__()
        self.api_url = "https://api.openai.com/v1/embeddings"
        self.model = "text-embedding-3-small"
        PaperTable.initialize_table()
        EmbeddingsTable.initialize_table()
        self.msg_queue = queue.Queue()
    
    def worker(self):
        while True:
            msg = self.msg_queue.get()
            if msg is None:
                break
            self.process_message(msg)
    
    def embedding_sequence(self):
        consumer = consume_topics(["scraper"], "scraper-group", pubsub = False)

        #start worker thread
        t = threading.Thread(target = self.worker)
        t.start()

        try:
            for message in consumer:
                self.msg_queue.put(message)
        except KeyboardInterrupt:
            logger.info("Interrupted by user.")
        finally:
            self.msg_queue.put(None)
            t.join()
        
    def execute(self, input: str):

        request_body = {
            "model": self.model,
            "input": input.replace("\n", " "),
        }

        response = self.post_request(self.api_url, request_body)

        return response['data'][0]['embedding']
    
    def process_message(self, message):
        logger.info(f"This is the result: {message.topic} | {message.key}: {message.value}")
        #data = json.loads(message.value)
        data = message.value
        logger.info(f"Process For {data['title']}")
        logger.info("Inserting into SQLLite")
        try:
            PaperTable.insert_paper(data['title'],
                                        data['authors'].replace(",",""),
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
        except:
            logger.info("Fail!")                


if __name__ == "__main__":
    test = Embedding()
    print(test.execute("Hello Vector!"))
        