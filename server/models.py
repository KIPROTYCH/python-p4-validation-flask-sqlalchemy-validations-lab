from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Name must not be empty.")
        return value

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be exactly ten digits.")
        return value

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    summary = db.Column(db.String(250))

    @validates('title')
    def validate_title(self, key, value):
        if not value:
            raise ValueError("Title is required.")
        clickbait_keywords = ['clickbait', 'sensational', 'shocking', 'exclusive']
        if any(keyword in value.lower() for keyword in clickbait_keywords):
            raise ValueError("Title contains clickbait content.")
        return value

    @validates('content')
    def validate_content_length(self, key, value):
        if len(value) <= 250:
            raise ValueError("Content must be at least 250 characters long.")
        return value

    @validates('summary')
    def validate_summary_length(self, key, value):
        if len(value) >= 250:
            raise ValueError("Summary cannot be more than 250 characters long.")
        return value

    @validates('category')
    def validate_category(self, key, value):
        allowed_categories = ['Fiction', 'Non-Fiction', 'Science Fiction', 'Mystery']
        if value not in allowed_categories:
            raise ValueError("Invalid category.")
        return value
