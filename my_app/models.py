import os
import jwt
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """This class represents the users table."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    backetlists = db.relationship(
        'Bucketlist', order_by='Bucketlist.id', cascade='all, delete-orphan')

    def __init__(self, username,email, password):
        """
        Initialize with username and password.
        """
        self.username = username
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id, app):
        """
        Generates the token.
        """
        try:
            """ set up a payload with an expiration time"""
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=30),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                "token_secret",
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # Decode the token using our SECRET variable
            payload = jwt.decode(token)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Bucketlist(db.Model):
    """This class represents the bucketlists table."""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    items = (db.relationship(
        'BucketlistItem', order_by='BucketlistItem.bucketlist_id',
        cascade='all, delete-orphan'))

    def __init__(self, name):
        """initialize with name."""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """
        Gets the bucketlists that belong to a aparticular user.
        """
        return Bucketlist.query.all()

    def delete(self):
        """
        Deletes a particular bucketlist.
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Bucketlist: {}>'.format(self.name)


class BucketlistItem(db.Model):
    """This class represents the bucketlist items table."""

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False, nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(
        Bucketlist.id), nullable=False)

    def __init__(self, name, bucketlist_id):
        """Initialize with name."""
        self.name = name
        self.bucketlist_id = bucketlist_id

    def save(self):
        """Save a new/edited bucketlist item"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Retrieve all the bucketlists items in a given bucketlist"""
        return BucketListItem.query.filter_by(BucketListItem.id)

    def delete(self):
        """Delete a bucketlist item"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<BucketlistItem: {}>'.format(self.name)
