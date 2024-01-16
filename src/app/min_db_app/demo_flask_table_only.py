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
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)
print(app.config['SQLALCHEMY_DATABASE_URI'])

## helper functions

def init_db():
    with app.app_context():
        db.create_all()
        print("Database tables created.")

def reset_db():
    """Drops and recreates the database tables."""
    with app.app_context():
        db.drop_all()  # Drops all tables
        db.create_all()  # Creates all tables
    print("Database tables reset.")

def list_tables():
    with app.app_context():
        inspector = db.inspect(db.engine)
        return inspector.get_table_names()


def list_columns(table_name):
    with app.app_context():
        inspector = db.inspect(db.engine)
        columns = inspector.get_columns(table_name)
        return [column['name'] for column in columns]



# Some dummy variables to spoof the login functionality



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


@app.route('/add_fish_capture', methods=['GET', 'POST'])
def add_fish_capture():
    # Custom function to populate the FishCapture class
    if request.method == 'POST':
        fish_capture = create_fish_capture()
        db.session.add(fish_capture)
        db.session.commit()
        flash('Your fish capture has been logged!')
        return redirect(url_for('display_captures'))
    
    return render_template('add_fish_capture.html')

def create_fish_capture():
    # Here you can add your custom logic to populate the FishCapture class
    user_id = 1
    lat = 36.7201600
    lng = -4.4203400
    fishing_spot_tag = "Mevagissey Harbour"
    tide_state = "HW+5"
    tide_coefficient = 76
    weather_conditions = "light rain"
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
    current_page_captures = FishCapture.query.order_by(FishCapture.timestamp).paginate(page=page, per_page=rows_per_page, error_out=False)


    return render_template('captures.html', captures=current_page_captures.items, page=page, total_pages=current_page_captures.pages)

@app.route('/list_tables')
def show_tables():
    tables = list_tables()
    return render_template('list_tables.html', tables=tables)

@app.route('/list_columns/<table_name>')
def show_columns(table_name):
    columns = list_columns(table_name)
    return render_template('list_columns.html', columns=columns, table_name=table_name)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
    
