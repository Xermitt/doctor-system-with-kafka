import os

def get_kafka_config():
    return {
        "bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
        "retries": int(os.getenv("KAFKA_RETRIES", 10)),
        "retry_delay": int(os.getenv("KAFKA_RETRY_DELAY", 5))
    }

def get_data_service_config():
    return {
        "url": os.getenv("DATA_SERVICE_URL", "http://data-service:5001"),
        "timeout": int(os.getenv("DATA_SERVICE_TIMEOUT", 5))
    }