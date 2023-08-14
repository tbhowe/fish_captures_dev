from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class FishCaptureForm(FlaskForm):
    GPS_location = StringField('GPS Location', validators=[DataRequired()])
    fishing_spot_tag = StringField('Fishing Spot Tag', validators=[DataRequired()])
    tide_state = StringField('Tide State', validators=[DataRequired()])
    weather_conditions = StringField('Weather Conditions', validators=[DataRequired()])
    daylight_state = StringField('Daylight State', validators=[DataRequired()])
    fish_type = StringField('Fish Type', validators=[DataRequired()])
    lure_bait_type = StringField('Lure/Bait Type', validators=[DataRequired()])
    submit = SubmitField('Submit')
