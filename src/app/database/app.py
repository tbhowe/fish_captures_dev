from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()
# Initialize Flask app
app = Flask(__name__)

# Database connection parameters
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Create the SQLALCHEMY_DATABASE_URI with SSL mode enabled
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

def list_db_tables(db):
    """
    Lists tables in the current database.
    :param db: The SQLAlchemy database instance from your Flask app.
    """
    engine = db.get_engine(app)
    with engine.connect() as conn:
        inspector = db.inspect(conn)
        tables = inspector.get_table_names()
        print("Tables in the database:")
        for table in tables:
            print(table)

# Initialize SQLAlchemy
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
# Initialize Flask-Login
login_manager = LoginManager(app)

# Import routes
from routes import *

from models import User  # Replace with your actual User model

@login_manager.user_loader
def load_user(user_id):
    # User.get(user_id) should retrieve the user's object from the database
    return User.query.get(int(user_id))


if __name__ == "__main__":
    app.run(debug=True)
    list_db_tables(db)