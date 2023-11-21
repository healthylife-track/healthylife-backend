import unittest
from flask import Flask, request, jsonify
from healthapp.models import User, db
from healthapp.routes import register

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test Flask app and create a test client
        app = Flask(__name__)
        app.config['TESTING'] = True
        self.app = app.test_client()
        # Create a test database
        db.create_all()

    def tearDown(self):
        # Clean up the test database
        db.session.remove()
        db.drop_all()

    def test_register_patient_success(self):
        # Test registration for a patient with valid data
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'patient',
            'phoneno': '1234567890',
            'licenseNo': 'None',
            'bloodgroup': 'A+',
        }

        response = self.app.post('/register', data=data)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['msg'], 'Registration Successful')

    def test_register_doctor_success(self):
        # Test registration for a doctor with valid data
        data = {
            'name': 'Dr. Smith',
            'email': 'smith@example.com',
            'role': 'doctor',
            'phoneno': '9876543210',
            'licenseNo': '123456',
            'bloodgroup': 'B-',
        }

        response = self.app.post('/register', data=data)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['msg'], 'Registration Successful')

    def test_register_missing_fields(self):
        # Test registration with missing fields
        data = {
            'name': '',
            'email': '',
            'role': '',
            'phoneno': '',
            'licenseNo': '',
            'bloodgroup': '',
        }

        response = self.app.post('/register', data=data)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['msg'], 'One or more field is empty')
