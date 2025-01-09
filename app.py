from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book  # Import db, Author, and Book from data_models.py
import os
from datetime import datetime
from sqlalchemy import asc, desc

# Ensure 'data' directory exists
os.makedirs('data', exist_ok=True)

app = Flask(__name__)

# Dynamically set the database URI using the current working directory
working_directory = os.getcwd()
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{working_directory}/data/library.sqlite'  #  relative path!!!!!!!!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # Required for flashing messages


# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Create tables if they don't exist
# with app.app_context():
#   try:
#     db.create_all()
#     print("Database tables created successfully!")
#   except Exception as e:
#     print(f"Error creating database tables: {e}")

# Home page route
@app.route('/')
def home():
    keyword = request.args.get('keyword', '').strip()
    sort_by = request.args.get('sort_by', 'title_asc')

    # Base query
    query = Book.query

    # Apply search filter if keyword is provided
    if keyword:
        query = query.join(Author).filter(
            (Book.title.ilike(f"%{keyword}%")) | (Author.name.ilike(f"%{keyword}%"))
        )

    # Apply sorting
    if sort_by == 'title_asc':
        query = query.order_by(Book.title.asc())
    elif sort_by == 'title_desc':
        query = query.order_by(Book.title.desc())
    elif sort_by == 'author_asc':
        query = query.join(Author).order_by(Author.name.asc())
    elif sort_by == 'author_desc':
        query = query.join(Author).order_by(Author.name.desc())

    books = query.all()

    # Flash a message if no books match the search criteria
    if keyword and not books:
        flash(f"No books found matching '{keyword}'.", "info")

    return render_template('home.html', books=books)

    
# Route to add an author
@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        birth_date = request.form.get('birth_date')
        date_of_death = request.form.get('date_of_death')

        # Convert dates to Python date objects
        try:
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date() if birth_date else None
            date_of_death = datetime.strptime(date_of_death, '%Y-%m-%d').date() if date_of_death else None
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "error")
            return redirect(url_for('add_author'))

        # Validate input
        if not name:
            flash("Author name is required!", "error")
            return redirect(url_for('add_author'))

        # Add new author to the database
        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death
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


# Route to add a book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Retrieve form data
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')

        # Validate input
        if not title or not isbn or not author_id:
            flash("All fields are required!", "error")
            return redirect(url_for('add_book'))

        # Add new book to the database
        new_book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            author_id=author_id
        )
        try:
            db.session.add(new_book)
            db.session.commit()
            flash(f"Book '{title}' added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding book: {str(e)}", "error")

        return redirect(url_for('add_book'))

    # Fetch authors for the dropdown menu
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


# The route will handle deleting a book and checking if the associated author has any other books.
# If not, it will delete the author as well.
@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    # Fetch the book by ID
    book = Book.query.get_or_404(book_id)
    author = book.author  # Get the associated author

    try:
        # Delete the book
        db.session.delete(book)

        # Check if the author has other books
        if len(author.books) == 1:  # Only this book exists
            db.session.delete(author)

        db.session.commit()
        flash(f"Book '{book.title}' and its author '{author.name}' were deleted successfully!" if len(author.books) == 1 else f"Book '{book.title}' was deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting book: {str(e)}", "error")

    return redirect(url_for('home'))



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)