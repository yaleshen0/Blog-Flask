"""
This file (test_users.py) contains the functional tests for the `auth_bp` blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the `auth_bp` blueprint.
"""
from werkzeug.security import generate_password_hash, check_password_hash

def test_login_page(test_client):
    """
    Given a Flask application configured for testing
    When the '/login' page is requested (GET)
    Then check the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Your Email' in response.data
    assert b'Your Password' in response.data
    assert b'Login' in response.data
    assert b'Register' in response.data

def test_invalid_login(test_client, init_database):
    """
    Given a Flask application configured for testing
    When the '/login' page is posted to with wrong password (POST)
    Then check an error message is returned to the user
    """
    response = test_client.post('/login',
                                data=dict(email='flaskkenny@gmail.com', password='flaskisawesome1'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Email and/or password not correct' in response.data
    assert b'Logout' not in response.data
    assert b'Login' in response.data
    assert b'Register' in response.data
    
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to with wrong email (POST)
    THEN check an error message is returned to the user
    """
    
    response = test_client.post('/login',
                                data=dict(email='flaskkenny1@gmail.com', password='flaskisawesome'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Email and/or password not correct' in response.data
    assert b'Logout' not in response.data
    assert b'Login' in response.data
    assert b'Register' in response.data

def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    When the '/login' page is posted to (POST)
    Then check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='flaskkenny@gmail.com', password='flaskisawesome'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome to the flask\'s blog' in response.data
    assert b'Add a post' in response.data
    assert b'Logout' in response.data
    
    """
    GIVEN a Flask application configured for testing
    When the '/logout' page is requested (GET)
    Then check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Logout successfully' in response.data
    assert b'Login' in response.data
    assert b'Your Email' in response.data
    assert b'Your Password' in response.data
    assert b'Login' in response.data
    assert b'Register' in response.data

def test_valid_registration(test_client, init_database):
    """
    Given a Flask application configured for testing
    When the '/signup' page is posted to (POST)
    Then check the response is valid and the user is logged in
    """
    response = test_client.post('/signup',
                                data=dict(name='flask',
                                          email='flaskkenny1@gmail.com',
                                          password='flaskisawesome'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Registered successfully' in response.data
    assert b'Login' in response.data
    assert b'Your Email' in response.data
    assert b'Your Password' in response.data
    assert b'Login' in response.data
    assert b'Register' in response.data

def test_duplicate_registration(test_client, init_database):
    """
    Given a Flask application configured for testing
    When the '/signup' page is posted to (POST) using an email address already registered
    Then check an error message is returned to the user
    """
    # Register the new account
    test_client.post('/signup',
                     data=dict(name='flask',
                               email='flask@hey.com',
                               password='FlaskIsTheBest'),
                     follow_redirects=True)

    # Try registering with the same email address
    response = test_client.post('/signup',
                                data=dict(name='flask',
                                          email='flask@hey.com',
                                          password='FlaskIsStillTheBest'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Email address already exists' in response.data
