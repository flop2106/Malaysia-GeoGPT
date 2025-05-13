import json
from kafka import KafkaProducer
import KafkaSetup
import time

from utils.LoggerBaseUtil import LoggerBaseUtil

logger = LoggerBaseUtil.get_logger()


def setupProducer(list_server: list[str] = ["localhost:9092"],
                  encoder: str = "utf-8") -> KafkaProducer:
    return (
    KafkaProducer(
    bootstrap_servers = list_server,
    key_serializer = lambda k: k.encode(encoder),
    value_serializer= lambda v: json.dumps(v).encode(encoder),
    api_version =(3,4)
    ))

def publish(producer: KafkaProducer, topic: str, key: str, payload: dict)-> None:
    count_try = 0
    while count_try< 3:
        try:
            future = producer.send(topic, key = key, value = payload)
            record_metadata = future.get(timeout = 30)
            logger.info(
            f"Published to {record_metadata.topic}"
            f"[partition {record_metadata.partition} @ offset {record_metadata.offset}]"            
            )
            count_try = 3
        except KafkaSetup.KafkaTimeoutError as e:
            logger.warning(f"Broker is not Controller: {e}. Retrying...")
            time.sleep(5)
            count_try +=1
        except Exception as e:
            logger.exception(f"Failed To Publish to {topic}: {e}")
            count_try +=1
    

if __name__ == "__main__":
    working_server = KafkaSetup.setup()
    #time.sleep(2)
    setup = setupProducer(list_server = [working_server])
    

    # example messages
    
    list_update = [
    ("price.technology",     "tech",   {"symbol": "NASDAQ",            "price": 650.34,          "ts": 1713657600}),
    ("news.economy",   "economy",{"headline": "Q1 GDP beats forecasts", "ts": 1713657600}),
    ("price.economy",  "economy",{"symbol": "US500",          "price": 4.21,            "ts": 1713657600}),
    ("news.technology",      "tech",   {"headline": "New AI chip unveiled",  "ts": 1713657600}),
    ]
    for args in list_update:
        publish(setup, *args)
        time.sleep(2)

    setup.flush()
    setup.close()