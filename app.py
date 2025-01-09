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
    
# Route to add an author
@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        birth_date = request.form.get('birth_date')
        date_of_death = request.form.get('date_of_death')

        # Validate input
        if not name:
            flash("Author name is required!", "error")
            return redirect(url_for('add_author'))

        # Add new author to the database
        new_author = Author(
            name=name,
            birth_date=birth_date if birth_date else None,
            date_of_death=date_of_death if date_of_death else None
        )
        try:
            db.session.add(new_author)
            db.session.commit()
            flash(f"Author '{name}' added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding author: {str(e)}", "error")

        return redirect(url_for('add_author'))

    # Render the form for GET requests
    return render_template('add_author.html')
