from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book  # Import db, Author, and Book from data_models.py
import os

# Ensure 'data' directory exists
os.makedirs('data', exist_ok=True)

app = Flask(__name__)

# Dynamically set the database URI using the current working directory
working_directory = os.getcwd()
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{working_directory}/data/library.sqlite'  #  relative path!!!!!!!!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
  try:
    db.create_all()
    print("Database tables created successfully!")
  except Exception as e:
    print(f"Error creating database tables: {e}")
