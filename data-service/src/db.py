import psycopg2
import logging
from .config import get_db_config

logger = logging.getLogger(__name__)

def connect_postgres():
    max_retries = 5
    db_config = get_db_config()
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                dbname=db_config["dbname"],
                user=db_config["user"],
                password=db_config["password"],
                host=db_config["host"],
                port=db_config["port"]
            )
            logger.info("Successfully connected to PostgreSQL")
            return conn
        except psycopg2.OperationalError as e:
            logger.warning(f"PostgreSQL not available, retrying... ({i+1}/{max_retries})")
            time.sleep(5)
    logger.error("Failed to connect to PostgreSQL after several attempts")
    raise Exception("PostgreSQL is unavailable")

def init_db():
    conn = None
    cursor = None
    try:
        conn = connect_postgres()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS appointments (
                id SERIAL PRIMARY KEY,
                patient_id INTEGER REFERENCES patients(id),
                doctor_name VARCHAR(100) NOT NULL,
                appointment_date DATE NOT NULL
            );
        """)
        conn.commit()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize PostgreSQL tables: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()