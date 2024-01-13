from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    """
    Form for users to log in.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """
    Form for new users to register.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def _validate_unique(self, field, model, field_name, error_message):
        """
        Helper method to validate unique fields.
        """
        record = model.query.filter_by(**{field_name: field.data}).first()
        if record:
            raise ValidationError(error_message)

    def validate_username(self, username):
        """
        Custom validation method to check if the provided username already exists in the database.
        """
        self._validate_unique(username, User, 'username', 'Please use a different username.')

    def validate_email(self, email):
        """
        Custom validation method to check if the provided email already exists in the database.
        """
        self._validate_unique(email, User, 'email', 'Please use a different email address.')

class FishCaptureForm(FlaskForm):
    """
    Form for users to record details of a fish capture.
    """
    GPS_location = StringField('GPS Location', validators=[DataRequired()])
    fishing_spot_tag = StringField('Fishing Spot Tag', validators=[DataRequired()])
    tide_state = StringField('Tide State', validators=[DataRequired()])
    weather_conditions = StringField('Weather Conditions', validators=[DataRequired()])
    daylight_state = StringField('Daylight State', validators=[DataRequired()])
    fish_type = StringField('Fish Type', validators=[DataRequired()])
    lure_bait_type = StringField('Lure/Bait Type', validators=[DataRequired()])
    submit = SubmitField('Submit')
