from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """
    User model representing registered users of the application.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    date_joined = db.Column(db.DateTime, default=db.func.current_timestamp())

    fish_captures = db.relationship('FishCapture', backref='user', lazy='dynamic')
    user_preferences = db.relationship('UserPreferences', backref='user', lazy='dynamic')

    def set_password(self, password):
        """
        Set the hashed version of the given password to the user.
        
        :param password: Plain-text password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the given password matches the stored hashed password.
        
        :param password: Plain-text password
        :return: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)

class FishCapture(db.Model):
    """
    FishCapture model representing the details of a fish capture event.
    """
    __tablename__ = 'fish_captures'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    GPS_location = db.Column(db.String(64))
    fishing_spot_tag = db.Column(db.String(64))
    tide_state = db.Column(db.String(64))
    weather_conditions = db.Column(db.String(64))
    daylight_state = db.Column(db.String(64))
    fish_type = db.Column(db.String(64))
    lure_bait_type = db.Column(db.String(64))

class UserPreferences(db.Model):
    """
    UserPreferences model representing the user's preferred settings and options.
    """
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    fish_button_1 = db.Column(db.String(64))
    fish_button_2 = db.Column(db.String(64))
    fish_button_3 = db.Column(db.String(64))
    lure_bait_options = db.Column(db.String(64))
