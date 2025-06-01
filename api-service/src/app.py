from flask import Flask
import logging
from .routes import setup_routes
from .kafka_producer import get_producer

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Инициализация продюсера Kafka
producer = get_producer()

# Настройка маршрутов
setup_routes(app, producer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)