from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from dotenv import load_dotenv
import os
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Database connection parameters
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?sslmode=require'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
db.create_all()

# Some dummy variables to spoof the login functionality
user_id = 1

## Create the Fishcapture model
class FishCapture(db.Model):
    """
    FishCapture model representing the details of a fish capture event.
    """
    __tablename__ = 'fish_captures'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer) #Add foreign key functionality later
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    GPS_location = db.Column(db.String(64))
    fishing_spot_tag = db.Column(db.String(64))
    tide_state = db.Column(db.String(64))
    tide_coefficient = db.Column(db.String(64))
    weather_conditions = db.Column(db.String(64))
    wind_speed = db.Column(db.Float)
    daylight_state = db.Column(db.String(64))
    fish_type = db.Column(db.String(64))
    lure_bait_type = db.Column(db.String(64))

class FishCaptureForm(FlaskForm):
    GPS_location = StringField('GPS Location', validators=[DataRequired()])
    fishing_spot_tag = StringField('Fishing Spot Tag', validators=[DataRequired()])
    tide_state = StringField('Tide State', validators=[DataRequired()])
    tide_coefficient = StringField('Tide Coefficient')
    weather_conditions = StringField('Weather Conditions', validators=[DataRequired()])
    wind_speed = StringField('Wind Speed')
    daylight_state = StringField('Daylight State', validators=[DataRequired()])
    fish_type = StringField('Fish Type', validators=[DataRequired()])
    lure_bait_type = StringField('Lure/Bait Type', validators=[DataRequired()])
    submit = SubmitField('Add Capture')



@app.route('/add_fish_capture', methods=['GET', 'POST'])
def add_fish_capture():
    """
    Render the fish capture addition page and handle fish capture addition logic.
    
    If the form is valid, add the fish capture to the database and redirect to the homepage.
    """
    form = FishCaptureForm()
    if form.validate_on_submit():
        fish_capture = FishCapture(user_id=user_id, GPS_location=form.GPS_location.data, fishing_spot_tag=form.fishing_spot_tag.data, tide_state=form.tide_state.data, weather_conditions=form.weather_conditions.data, daylight_state=form.daylight_state.data, fish_type=form.fish_type.data, lure_bait_type=form.lure_bait_type.data)
        db.session.add(fish_capture)
        db.session.commit()
        flash('Your fish capture has been added!')
        return redirect(url_for('index'))
    return render_template('add_fish_capture.html', title='Add Fish Capture', form=form)

@app.route('/')
def display_captures():
    page = int(request.args.get('page', 1))
    rows_per_page = 25

    # Fetch a subset of data for the current page using Flask SQLAlchemy
    current_page_captures = FishCapture.query.order_by(FishCapture.timestamp).paginate(page, rows_per_page, False)

    return render_template('captures.html', captures=current_page_captures.items, page=page, total_pages=current_page_captures.pages)
