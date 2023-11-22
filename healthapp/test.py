import unittest
from flask import Flask, request, jsonify
from healthapp import app, db
from healthapp.models import User, Login
from healthapp.routes import register, login
  
    
class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test Flask app and create a test client
        app = Flask(__name__)
        app.config['TESTING'] = True
        self.app = app.test_client(use_cookies=True)
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

    """ test for login"""
    
    def setUp(self):
        self.app = app.test_client()

    def test_login_with_empty_fields(self):
        response = self.app.post('/login/', json={'email': '', 'pwd': ''})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'One or more field is empty')

    def test_login_with_invalid_credentials(self):
        # Assuming you have a test user in your database with known credentials
        test_user = User(user_email='test@example.com', user_pass='hashed_password')
        db.session.add(test_user)
        db.session.commit()

        response = self.app.post('/login/', json={'email': 'test@example.com', 'pwd': 'wrong_password'})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'kindly supply a valid email address and password')

    def test_successful_login(self):
        # Assuming you have a test user in your database with known credentials
        test_user = User(user_email='test@example.com', user_pass='hashed_password')
        db.session.add(test_user)
        db.session.commit()

        response = self.app.post('/login/', json={'email': 'test@example.com', 'pwd': 'correct_password'})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'Login successful')
        # Additional assertions to check if the user is logged in and the login record is added to the database


    """test for logout"""

    def setUp(self):
        self.app = app.test_client()
        # Assuming you have a test user in your database with a known user_id
        self.loggedin_user_id = 1

        # Create a test login record for the user
        test_login = Login(login_userid=self.loggedin_user_id)
        db.session.add(test_login)
        db.session.commit()

    def test_successful_logout(self):
        # Set the user in the session to simulate a logged-in state
        with self.app.session_transaction() as session:
            session['user'] = self.loggedin_user_id

        response = self.app.get('/logout/')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'You have successfully logout')

        # Additional assertions to check if the logout date is updated in the database
        logout_record = Login.query.filter_by(login_userid=self.loggedin_user_id).first()
        self.assertIsNotNone(logout_record.logout_date)

    def test_logout_without_logged_in_user(self):
        response = self.app.get('/logout/')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'You have successfully logout')

        # Additional assertions to check if the logout date is not updated in the database
        logout_record = Login.query.filter_by(login_userid=self.loggedin_user_id).first()
        self.assertIsNone(logout_record.logout_date)