from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import time
import logging
from .config import get_kafka_config

logger = logging.getLogger(__name__)

def connect_kafka_producer():
    config = get_kafka_config()
    retries = config["retries"]
    for i in range(retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=config["bootstrap_servers"],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            logger.info("Successfully connected to Kafka")
            return producer
        except NoBrokersAvailable:
            logger.warning(f"Kafka not available, retrying... ({i+1}/{retries})")
            time.sleep(config["retry_delay"])
    logger.error("Failed to connect to Kafka after several attempts")
    raise Exception("Kafka is unavailable")

def get_producer():
    try:
        return connect_kafka_producer()
    except Exception as e:
        logger.error(f"Failed to initialize Kafka producer: {str(e)}")
        return None