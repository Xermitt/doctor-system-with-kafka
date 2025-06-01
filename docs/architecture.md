# System Architecture

## Overview
The system is a microservices-based application for managing doctor appointments, built with Docker, Kafka, and PostgreSQL.

## Components
- **API Service**: Handles HTTP requests, sends data to Kafka.
- **Data Service**: Consumes data from Kafka, stores it in PostgreSQL, and provides search/report endpoints.
- **Kafka**: Message broker for asynchronous communication.
- **Zookeeper**: Coordinates Kafka cluster.
- **PostgreSQL**: Stores appointment data.

## Data Flow
1. User sends a POST request to API Service to add an appointment.
2. API Service sends the data to Kafka topic `appointments`.
3. Data Service consumes the data from Kafka and stores it in PostgreSQL.
4. User can search or generate reports via GET requests, which API Service proxies to Data Service.