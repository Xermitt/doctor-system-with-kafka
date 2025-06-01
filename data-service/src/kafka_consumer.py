from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
import time
import logging
from .config import get_kafka_config
from .db import connect_postgres

logger = logging.getLogger(__name__)

def connect_kafka_consumer():
    config = get_kafka_config()
    retries = config["retries"]
    for i in range(retries):
        try:
            consumer = KafkaConsumer(
                'appointments',
                bootstrap_servers=config["bootstrap_servers"],
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            logger.info("Successfully connected to Kafka")
            return consumer
        except NoBrokersAvailable:
            logger.warning(f"Kafka not available, retrying... ({i+1}/{retries})")
            time.sleep(config["retry_delay"])
    logger.error("Failed to connect to Kafka after several attempts")
    raise Exception("Kafka is unavailable")

def consume_kafka_messages():
    consumer = connect_kafka_consumer()
    for message in consumer:
        try:
            data = message.value
            if not all(key in data for key in ['patient_name', 'doctor_name', 'appointment_date']):
                logger.warning(f"Invalid data from Kafka: {data}")
                continue
            conn = connect_postgres()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO patients (name) VALUES (%s) RETURNING id",
                          (data['patient_name'],))
            patient_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO appointments (patient_id, doctor_name, appointment_date) VALUES (%s, %s, %s)",
                          (patient_id, data['doctor_name'], data['appointment_date']))
            conn.commit()
            logger.info(f"Inserted appointment for patient {data['patient_name']} with doctor {data['doctor_name']}")
        except Exception as e:
            logger.error(f"Failed to process Kafka message: {str(e)}")
            if 'conn' in locals():
                conn.rollback()
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()