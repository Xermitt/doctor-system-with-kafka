from flask import jsonify, request
import requests
import logging
from .config import get_data_service_config

logger = logging.getLogger(__name__)

def setup_routes(app, producer):
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An internal error occurred", "message": str(e)}), 500

    @app.route('/api/appointment', methods=['POST'])
    def add_appointment():
        if not producer:
            return jsonify({"error": "Kafka service is unavailable"}), 503
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        data = request.json
        required_fields = ['patient_name', 'doctor_name', 'appointment_date']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        try:
            producer.send('appointments', data)
            return jsonify({"message": "Appointment added"}), 201
        except Exception as e:
            logger.error(f"Failed to send to Kafka: {str(e)}")
            return jsonify({"error": "Failed to process appointment"}), 500

    @app.route('/api/search', methods=['GET'])
    def search_appointments():
        params = {
            "patient_name": request.args.get('patient_name'),
            "date": request.args.get('date')
        }
        config = get_data_service_config()
        try:
            response = requests.get(f"{config['url']}/api/search", params=params, timeout=config["timeout"])
            response.raise_for_status()
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to data-service: {str(e)}")
            return jsonify({"error": "Data service is unavailable"}), 503

    @app.route('/api/report/top-doctors', methods=['GET'])
    def top_doctors():
        config = get_data_service_config()
        try:
            response = requests.get(f"{config['url']}/api/report/top-doctors", timeout=config["timeout"])
            response.raise_for_status()
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to data-service: {str(e)}")
            return jsonify({"error": "Data service is unavailable"}), 503

    @app.route('/api/report/appointments-per-day', methods=['GET'])
    def appointments_per_day():
        config = get_data_service_config()
        try:
            response = requests.get(f"{config['url']}/api/report/appointments-per-day", timeout=config["timeout"])
            response.raise_for_status()
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to data-service: {str(e)}")
            return jsonify({"error": "Data service is unavailable"}), 503

    @app.route('/api/report/top-patients', methods=['GET'])
    def top_patients():
        config = get_data_service_config()
        try:
            response = requests.get(f"{config['url']}/api/report/top-patients", timeout=config["timeout"])
            response.raise_for_status()
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to data-service: {str(e)}")
            return jsonify({"error": "Data service is unavailable"}), 503