# API Documentation

## API Service
### POST /api/appointment
- **Description**: Add a new appointment.
- **Request Body**:
  ```json
  {
      "patient_name": "string",
      "doctor_name": "string",
      "appointment_date": "YYYY-MM-DD"
  }