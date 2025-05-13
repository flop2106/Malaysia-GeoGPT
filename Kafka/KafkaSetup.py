from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, KafkaTimeoutError
import time
from utils.LoggerBaseUtil import LoggerBaseUtil

logger = LoggerBaseUtil.get_logger()

def setup(listServer: list[str] = ["localhost:9092",],
          clientId: str = "admin_demo",
          topicName: list[str] = ["news.economy", "price.economy", "news.technology", "price.technology"],
          topicPartitions: list[int] = [1,1,1,1],
          topicRF: list[int] = [1,1,1,1]) -> None:
          
    topics = []
    for idx, val in enumerate(topicName):
        topics.append(NewTopic(name = val, 
                               num_partitions = topicPartitions[idx],
                               replication_factor = topicRF[idx]))
    # Create topic if not exists
    for attempt in listServer:
        try:
            admin = KafkaAdminClient(
                    bootstrap_servers = [attempt],
                    client_id = clientId,
                    api_version =(3,4)
                    )
            admin.create_topics(new_topics = topics, validate_only = False)
            logger.info("Topic Created successfully")
            admin.close()
            return attempt
        except TopicAlreadyExistsError as e:
            logger.info(f"Already Exists Error: {e}")
            admin.close()
            return attempt
        except KafkaTimeoutError as e:
            logger.warning(f"Broker is not Controller: {e}. Retrying...")
            time.sleep(1)
            continue
        except Exception as e:
            logger.info(f"Errors in creating Topics: {e}")
    
    return None
        

if __name__=="__main__":
    working_server = setup()
    print(f"Working server: {working_server}")