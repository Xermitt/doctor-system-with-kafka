from flask import jsonify, request
from datetime import datetime
import logging
from .db import connect_postgres

logger = logging.getLogger(__name__)

def setup_routes(app):
    @app.route('/api/search', methods=['GET'])
    def search_appointments():
        conn = None
        cursor = None
        try:
            conn = connect_postgres()
            cursor = conn.cursor()
            patient_name = request.args.get('patient_name')
            date = request.args.get('date')
            
            query = """
                SELECT p.name, a.doctor_name, a.appointment_date
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                WHERE 1=1
            """
            params = []
            
            if patient_name:
                query += " AND p.name ILIKE %s"
                params.append(f"%{patient_name}%")
            if date:
                query += " AND a.appointment_date = %s"
                params.append(date)
                
            cursor.execute(query, params)
            results = cursor.fetchall()
            return jsonify([{
                "patient_name": row[0],
                "doctor_name": row[1],
                "appointment_date": row[2].strftime('%Y-%m-%d')
            } for row in results])
        except Exception as e:
            logger.error(f"Search query failed: {str(e)}")
            return jsonify({"error": "Failed to perform search"}), 500
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @app.route('/api/report/top-doctors', methods=['GET'])
    def top_doctors():
        conn = None
        cursor = None
        try:
            conn = connect_postgres()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT doctor_name, COUNT(*) as appointment_count
                FROM appointments
                GROUP BY doctor_name
                ORDER BY appointment_count DESC
                LIMIT 10
            """)
            results = cursor.fetchall()
            return jsonify([{
                "doctor_name": row[0],
                "appointment_count": row[1]
            } for row in results])
        except Exception as e:
            logger.error(f"Top doctors report failed: {str(e)}")
            return jsonify({"error": "Failed to generate report"}), 500
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @app.route('/api/report/appointments-per-day', methods=['GET'])
    def appointments_per_day():
        conn = None
        cursor = None
        try:
            conn = connect_postgres()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT appointment_date, COUNT(*) as appointment_count
                FROM appointments
                GROUP BY appointment_date
                ORDER BY appointment_date
            """)
            results = cursor.fetchall()
            return jsonify([{
                "date": row[0].strftime('%Y-%m-%d'),
                "appointment_count": row[1]
            } for row in results])
        except Exception as e:
            logger.error(f"Appointments per day report failed: {str(e)}")
            return jsonify({"error": "Failed to generate report"}), 500
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @app.route('/api/report/top-patients', methods=['GET'])
    def top_patients():
        conn = None
        cursor = None
        try:
            conn = connect_postgres()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.name, COUNT(a.id) as appointment_count
                FROM patients p
                JOIN appointments a ON p.id = a.patient_id
                GROUP BY p.name
                ORDER BY appointment_count DESC
                LIMIT 10
            """)
            results = cursor.fetchall()
            return jsonify([{
                "patient_name": row[0],
                "appointment_count": row[1]
            } for row in results])
        except Exception as e:
            logger.error(f"Top patients report failed: {str(e)}")
            return jsonify({"error": "Failed to generate report"}), 500
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()