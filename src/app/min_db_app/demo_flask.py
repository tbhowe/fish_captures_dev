from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from uuid import uuid4
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database connection parameters
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Create the SQLALCHEMY_DATABASE_URI with SSL mode enabled
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the example model
class Example(db.Model):
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    uuid = db.Column(db.String, primary_key=True)

# Create the tables
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/create_table')
def create_table():
    create_tables()  # This will create all tables
    return 'Table created'

@app.route('/insert_record')
def insert_record():
    new_record = Example(uuid=str(uuid4()))
    db.session.add(new_record)
    db.session.commit()
    return f'Record inserted: {new_record.uuid}'

@app.route('/delete_record/<uuid_str>')
def delete_record(uuid_str):
    record = Example.query.filter_by(uuid=uuid_str).first()
    if record:
        db.session.delete(record)
        db.session.commit()
        return f'Record deleted: {uuid_str}'
    else:
        return 'Record not found'

if __name__ == '__main__':
    app.run(debug=True)
