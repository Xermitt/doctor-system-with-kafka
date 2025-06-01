import os

def get_db_config():
    return {
        "dbname": os.getenv("POSTGRES_DB", "doctor_appointments"),
        "user": os.getenv("POSTGRES_USER", "admin"),
        "password": os.getenv("POSTGRES_PASSWORD", "password"),
        "host": os.getenv("DB_HOST", "postgres"),
        "port": os.getenv("DB_PORT", "5432")
    }

def get_kafka_config():
    return {
        "bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
        "retries": int(os.getenv("KAFKA_RETRIES", 10)),
        "retry_delay": int(os.getenv("KAFKA_RETRY_DELAY", 5))
    }