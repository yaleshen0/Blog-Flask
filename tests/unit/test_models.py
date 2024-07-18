from src.models.user import User
from src.models.post import Post
from werkzeug.security import generate_password_hash, check_password_hash

def test_new_user(new_user):
    """
    Given a User model
    When a new User is created
    Then check the name, the email, hashed_password are defined correctly
    """
    assert new_user.name == 'flask'
    assert new_user.email == 'flaskkenny@gmail.com'
    assert generate_password_hash(new_user.password) != 'flaskisawesome'
    assert new_user.__repr__() == '<User flask email address: flaskkenny@gmail.com>'
    assert new_user.is_authenticated
    assert new_user.is_active

def test_new_post(new_post):
    """
    Given a Post model
    WHEN a new Book is created
    THEN check the title, author, and rating fields are defined correctly
    """
    assert new_post.title == 'flask factory application'
    assert new_post.content == 'You can have multiple instances of the same application running in the same app process'
    assert new_post.created_by == 1
    assert new_post.__repr__() == '<Post flask factory application: by 1>'

