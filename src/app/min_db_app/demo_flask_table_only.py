from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from dotenv import load_dotenv
import os
import uuid
import datetime

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
lat = 36.7201600
lng = -4.4203400

## Create the Fishcapture model
class FishCapture(db.Model):
    """
    FishCapture model representing the details of a fish capture event.
    """
    __tablename__ = 'fish_captures'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer) #Add foreign key functionality later
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    fishing_spot_tag = db.Column(db.String(64))
    tide_state = db.Column(db.String(64))
    tide_coefficient = db.Column(db.Integer)
    weather_conditions = db.Column(db.String(64))
    wind_speed = db.Column(db.Float)
    wind_direction = db.Column(db.String(64))
    daylight_state = db.Column(db.String(64))
    fish_type = db.Column(db.String(64))
    lure_bait_type = db.Column(db.String(64))


@app.route('/add_fish_capture', methods=['POST'])
def add_fish_capture():
    # Custom function to populate the FishCapture class
    fish_capture = create_fish_capture()
    db.session.add(fish_capture)
    db.session.commit()
    flash('Your fish capture has been logged!')
    return redirect(url_for('display_captures'))

def create_fish_capture():
    # Here you can add your custom logic to populate the FishCapture class
    id = uuid.uuid4()
    user_id = user_id
    lat= lat
    lng = lng
    fishing_spot_tag = "Mevagissey Harbour"
    tide_state = "HW+5"
    tide_coefficient = 76
    weather_conditions = db.Column(db.String(64))
    wind_speed = 14.2
    wind_direction = "SW"
    daylight_state = "civil twilight (Dawn)"
    fish_type = "european bass > 60cm"
    lure_bait_type = "SG seeker 28g"
    return FishCapture(user_id=user_id, timestamp=datetime.datetime.now(), lat=lat, lng=lng, fishing_spot_tag=fishing_spot_tag, tide_state=tide_state, tide_coefficient=tide_coefficient, weather_conditions=weather_conditions, wind_speed=wind_speed, wind_direction=wind_direction, daylight_state=daylight_state, fish_type=fish_type, lure_bait_type=lure_bait_type)



@app.route('/')
def display_captures():
    page = int(request.args.get('page', 1))
    rows_per_page = 25

    # Fetch a subset of data for the current page using Flask SQLAlchemy
    current_page_captures = FishCapture.query.order_by(FishCapture.timestamp).paginate(page, rows_per_page, False)

    return render_template('captures.html', captures=current_page_captures.items, page=page, total_pages=current_page_captures.pages)
