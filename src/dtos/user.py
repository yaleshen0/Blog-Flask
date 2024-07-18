from ..models.user import User
from src import db

class UserDTO:
    def __init__(self, model):
        self.mode = model

    # create a user
    def create_user(self, new_user: User):
        db.session.add(new_user)
        db.session.commit()
    # get a user by email
    def get_by_email(self, email: str):
        return (
            User.query.filter_by(email=email).first()
        )
user_dto = UserDTO(User)