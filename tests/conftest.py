import pytest
from datetime import datetime
from src import create_app
from src import db
from src.models.user import User
from src.models.post import Post
from werkzeug.security import generate_password_hash, check_password_hash
# --------
# Fixtures
# --------

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def new_user():
    user = User('flask', 'flaskkenny@gmail.com', generate_password_hash('flaskisawesome'))
    return user

@pytest.fixture(scope='module')
def new_post():
    post = Post('flask factory application', 
                'You can have multiple instances of the same application running in the same app process', 
                datetime.now(), 
                1)
    return post
    
@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    default_user = User(name='flask', email='flaskkenny@gmail.com', password=generate_password_hash('flaskisawesome'))
    second_user = User(name='fiona', email='fionaw@yahoo.com', password=generate_password_hash('fionaisawesome'))
    db.session.add(default_user)
    db.session.add(second_user)

    # Commit the changes for the users
    db.session.commit()

    # Insert book data
    post_1 = Post('Glad to be here', 'Hello WOrld', datetime.now(), default_user.id)
    post_2 = Post('Todays weather: sunny', 'i learnt flask today', datetime.now(), default_user.id)
    post_3 = Post('Reference', 'Flask documentation', datetime.now(), default_user.id)
    post_4 = Post('I am the first', 'HELLO World!', datetime.now(), second_user.id)
    db.session.add(post_1)
    db.session.add(post_2)
    db.session.add(post_3)
    db.session.add(post_4)

    # Commit the changes for the books
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

@pytest.fixture(scope='function')
def log_in_default_user(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    default_user = User(name='flask', email='flaskkenny@gmail.com', password=generate_password_hash('flaskisawesome'))
    db.session.add(default_user)
    
    # Commit the changes for the users
    db.session.commit()

    test_client.post('/login',
                     data={'email': 'flaskkenny@gmail.com', 'password': 'flaskisawesome'})

    yield  # this is where the testing happens!

    test_client.get('/logout')
    db.drop_all()

@pytest.fixture(scope='module')
def cli_test_client():
    # Set the Testing configuration prior to creating the Flask application
    flask_app = create_app('testing')

    runner = flask_app.test_cli_runner()

    yield runner  # this is where the testing happens!

