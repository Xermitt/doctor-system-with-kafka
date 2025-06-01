# Doctor Appointment System

## Описание

Проект представляет собой микросервисную систему для управления записями к врачам.  
Данные обрабатываются через Kafka и сохраняются в PostgreSQL.  
Система реализована с использованием Python (Flask), Docker и Kafka.

---

## Архитектура

Система состоит из следующих компонентов:

- API Service (api-service) — REST API, принимает HTTP-запросы и отправляет данные в Kafka.
- Data Service (data-service) — получает сообщения из Kafka, сохраняет данные в PostgreSQL и предоставляет отчёты.
- Kafka + Zookeeper — брокер сообщений.
- PostgreSQL — база данных для хранения записей.
- Всё развернуто в Docker-контейнерах через docker-compose.

---

## Как запустить

1. Клонируйте репозиторий и перейдите в корневую директорию проекта:
   ```bash
   git clone https://github.com/Xermitt/doctor-system-with-kafka.git
   
   cd docApp
2. Создайте файл .env в корневой директории:
  POSTGRES_USER=admin
  POSTGRES_PASSWORD=password
  POSTGRES_DB=doctor_appointments
  DB_HOST=postgres
  DB_PORT=5432
  KAFKA_BOOTSTRAP_SERVERS=kafka:9092
  KAFKA_RETRIES=10
  KAFKA_RETRY_DELAY=5
  DATA_SERVICE_URL=http://data-service:5001
  DATA_SERVICE_TIMEOUT=5
3. Запустите систему:
    docker compose up --build

4. Готово! Сервисы будут доступны по адресам:
API Service: http://localhost:5000
Data Service: http://localhost:5001
PostgreSQL: доступен внутри сети (user: admin, pass: password, db: doctor_appointments)

Примеры запросов
Добавить запись (POST)
POST http://localhost:5000/api/appointment
Content-Type: application/json
    {
      "patient_name": "Иван Иванов",
      "doctor_name": "Доктор Смирнов",
      "appointment_date": "2025-06-01"
    }


Получить записи (GET)
GET http://localhost:5000/api/search?patient_name=Иван


Топ-10 популярных врачей
GET http://localhost:5000/api/report/top-doctors



Записи по дням
GET http://localhost:5000/api/report/appointments-per-day

Стек технологий
Python 3.9 + Flask
Apache Kafka
PostgreSQL
Docker + Docker Compose
Pytest