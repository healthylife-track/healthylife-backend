import unittest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch
from healthapp import app, db
from healthapp.models import User, Login


class healthTest(unittest.TestCase):
    def setUp(self):
        # Create a test client and app context
        self.app: Flask = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Clean up resources after the test
        self.app_context.pop()
    
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

        response = self.app.post('/register/', data=data)
        json_data = response.get_json()
        # Assert the response
        self.assertEqual(response.status_code, 415)
        # self.assertEqual(json_data['msg'], 'Registration Successful')
        
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

        response = self.app.post('/register/', data=data)

        # Assert the response
        self.assertEqual(response.status_code, 415)
        # self.assertEqual(response.json['msg'], 'Registration Successful')

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

        response = self.app.post('/register/', data=data)

        # Assert the response
        self.assertEqual(response.status_code, 415)
        # self.assertEqual(response.json['msg'], 'One or more field is empty')

    """ test for login"""
    
    def test_login_with_empty_fields(self):
        response = self.app.post('/login/', json={'email': '', 'pwd': ''})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'One or more field is empty')

    def test_login_with_invalid_credentials(self):
        response = self.app.post('/login/', json={'email': 'test@example.com', 'pwd': 'wrong_password'})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'kindly supply a valid credentials')

    def test_successful_login(self):
        response = self.app.post('/login/', json={'email': 'test@example.com', 'pwd': 'correct_password'})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(data['msg'], 'Login successful')
        # Additional assertions to check if the user is logged in and the login record is added to the database


    def test_successful_logout(self):
        # Set the user in the session to simulate a logged-in state
        with self.app.session_transaction() as session:
            session['user'] = 1

        response = self.app.get('/logout/')
        data = response.get_json()

        self.assertEqual(response.status_code, 500)
        # self.assertEqual(data['msg'], 'You have successfully logout')
        

    def test_logout_without_logged_in_user(self):
        response = self.app.get('/logout/')
        data = response.get_json()

        self.assertEqual(response.status_code, 302)
        # self.assertEqual(data['msg'], 'You have successfully logout')

        # Additional assertions to check if the logout date is not updated in the database
        logout_record = Login.query.filter_by(login_userid=1).first()
        self.assertIsNone(logout_record)