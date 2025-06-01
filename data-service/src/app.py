from flask import Flask
import logging
import threading
from .routes import setup_routes
from .kafka_consumer import consume_kafka_messages
from .db import init_db

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Инициализация базы данных
init_db()

# Запускаем Kafka consumer в отдельном потоке
kafka_thread = threading.Thread(target=consume_kafka_messages, daemon=True)
kafka_thread.start()

# Настройка маршрутов
setup_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)