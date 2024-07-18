from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy
from src import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = "Post"

    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    title = db.Column(db.String(150),nullable=False)
    content = db.Column(db.Text,nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    created_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, title, content, created_at, created_by):
        self.title = title
        self.content = content
        self.created_at = created_at
        self.created_by = created_by

    def __repr__(self):
        return f'<Post {self.title}: by {self.created_by}>'