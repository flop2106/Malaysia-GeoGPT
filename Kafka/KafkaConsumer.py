import threading
import json
from kafka import KafkaConsumer
import time
from utils.LoggerBaseUtil import LoggerBaseUtil

logger = LoggerBaseUtil.get_logger()


def safe_json_deserializer(m):
    try:
        return json.loads(m.decode("utf-8"))
    except Exception as e:
        logger.warning(f"Broker not ready - retrying in 3s...: {e}")
        return None

def consume_topics(topics: list[str],
                   group_id : str = "news-price-group",
                   bootstrap_servers:list[str] = ["localhost:9092"], 
                ) -> None:
    consumer = KafkaConsumer(
        *topics,
        bootstrap_servers = bootstrap_servers,
        group_id = group_id,
        value_deserializer = safe_json_deserializer,
        key_deserializer = lambda m: m.decode("utf-8") if m else None,
        enable_auto_commit = True,
    )
    logger.info(f"Started listening to: {topics}")
    return consumer