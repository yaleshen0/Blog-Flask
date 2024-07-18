from src import create_app
import os
from datetime import datetime
from flask_login import current_user

def test_post(test_client, log_in_default_user):
    """
    Given a flask application configured for testing
    When the '/' page is requested (GET)
    Then check the response is valid
    """
    response = test_client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome to the flask\'s blog' in response.data 
    assert b'Add a post' in response.data

def test_post_post(test_client):
    """
    Given a flask application configured for testing
    When the '/' page is requested (POST)
    Then check the response is valid
    """
    response = test_client.post('/')
    assert response.status_code == 405
    assert b"405 Method Not Allowed" in response.data

def test_create_post(test_client, log_in_default_user):
    """
    Given a Flask application configured for testing and the user logged in
    When the '/create' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.get('/create', 
                               follow_redirects=True)
    assert response.status_code == 200
    assert b'Title' in response.data
    assert b'Content' in response.data
    assert b'Back' in response.data
    assert b'Create' in response.data

def test_create_post_not_logged_in(test_client):
    """
    Given a Flask application configured for testing
    When the '/create' page is posted to (POST) when the user is not logged in
    Then check that the user is redirected to the login page
    """
    response = test_client.get('/create', follow_redirects=True)
    assert response.status_code == 200
    assert b'Create' not in response.data
    assert b'Login' in response.data
    
def test_get_post(test_client, log_in_default_user):
    """
    Given a Flask application configured for testing and the user logged to post a post
    When the '/<int:post_id>' page is requested (GET)
    Then check that the post was displayed successfully
    """
    test_client.post('/create',
                                data={'title': 'today is great',
                                      'content': 'I went to time square',
                                      'created_at': datetime.now(),
                                      'created_by': current_user.id},
                                follow_redirects=True)
    response = test_client.get('/1')
    assert response.status_code == 200
    assert b'today is great' in response.data
    assert b'I went to time square' in response.data
    assert b'Back' in response.data
    assert b'Update' in response.data

def test_get_post_not_logged_in(test_client, log_in_default_user):
    """
    Given a Flask application configured for testing and the user logged to post a post
    When the '/<int:post_id>' page is requested (GET)
    Then check that the post was displayed successfully
    """
    test_client.post('/create',
                    data={'title': 'today is great',
                          'content': 'I went to time square',
                          'created_at': datetime.now(),
                          'created_by': current_user.id},
                    follow_redirects=True)
    test_client.get('/logout')
    response = test_client.get('/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'today is great' not in response.data
    assert b'Login' in response.data

def test_update_post(test_client, init_database):
    """
    Given a Flask application configured for testing and the user logged in
    When the '/<int:post_id>/update' page is posted (POST)
    THEN check the response is valid
    """
    test_client.post('/login',
                     data={'email': 'flaskkenny@gmail.com', 'password': 'flaskisawesome'})
    test_client.get('/1')
    response = test_client.post('/1/update',
                                data={'title': 'I just changed my mind',
                                      'content': 'I just changed the content'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Glad to be here' not in response.data
    assert b'I just changed my mind' in response.data
    assert b'I just changed the content' in response.data

def test_update_post_not_logged_in(test_client, init_database):
    """
    Given a Flask application configured for testing when the user is not logged in
    When the '/<int:post_id>/update' page is posted (POST)
    Then check that the user is redirected to the login page
    """
    test_client.get('/logout')
    response = test_client.post('/1/update',
                    data={'title': 'I just changed my title',
                          'content': 'Content updated'},
                    follow_redirects=True)
    assert response.status_code == 200
    assert b'Glad to be here' not in response.data
    assert b'Login' in response.data

def test_delete_post(test_client, init_database):
    """
    Given a Flask application configured for testing when the user is logged in
    When the '/<int:post_id>/delete' page is posted (POST)
    Then check the response is valid
    """
    test_client.post('/login',
                     data={'email': 'flaskkenny@gmail.com', 'password': 'flaskisawesome'})
    response = test_client.post('/1/delete',
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Glad to be here' not in response.data

def test_delete_post_not_logged_in(test_client):
    """
    Given a Flask application configured for testing when the user is not logged in
    When the '/<int:post_id>/delete' page is posted (POST)
    Then check the response is valid
    """
    test_client.post('/create',
                    data={'title': 'today is great',
                          'content': 'I went to time square',
                          'created_at': datetime.now(),
                          'created_by': current_user.id},
                    follow_redirects=True)
    test_client.get('/logout')
    response = test_client.post('/1/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data