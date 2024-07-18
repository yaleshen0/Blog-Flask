from src import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto') # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f'<User {self.name} email address: {self.email}>'
    
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_email(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated
    
    def is_anonymous(self):
        """All users are not anonymous"""
        return False