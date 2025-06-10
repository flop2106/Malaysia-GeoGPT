import threading
import json
from kafka import KafkaConsumer, TopicPartition
import time
import utils.LoggerBaseUtil as LoggerBaseUtil

logger = LoggerBaseUtil.setup()


def safe_json_deserializer(m):
    try:
        return json.loads(m.decode("utf-8"))
    except Exception as e:
        logger.warning(f"Broker not ready - retrying in 3s...: {e}")
        return None

def consume_topics(
                   topics: list[str],
                   group_id : str = "news-price-group",
                   bootstrap_servers:list[str] = ["localhost:9092"], 
                   pubsub: bool = True,
                ) -> KafkaConsumer:
    if pubsub == True:
        consumer = KafkaConsumer(
            *topics,
            bootstrap_servers = bootstrap_servers,
            group_id = group_id,
            value_deserializer = safe_json_deserializer,
            key_deserializer = lambda m: m.decode("utf-8") if m else None,
            enable_auto_commit = True,
            auto_offset_reset = "earliest",
            api_version = (3,4),
            consumer_timeout_ms = 10000,
        )
        logger.info(f"Started listening to: {topics}")
    else:
        consumer = KafkaConsumer(
            bootstrap_servers = bootstrap_servers,
            value_deserializer = safe_json_deserializer,
            key_deserializer = lambda m: m.decode("utf-8") if m else None,
            enable_auto_commit = False,
            auto_offset_reset = "earliest",
        )
        tp = TopicPartition(topics[0], 0)
        consumer.assign([tp])
    return consumer