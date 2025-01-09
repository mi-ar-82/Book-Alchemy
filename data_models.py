from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'  # Optional: Specify the table name explicitly

    # Attributes
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-incrementing PK
    name = db.Column(db.String(100), nullable=False)  # Name of the author
    birth_date = db.Column(db.Date, nullable=True)  # Birth date (optional)
    date_of_death = db.Column(db.Date, nullable=True)  # Date of death (optional)

    # String representation for debugging or display purposes
    def __repr__(self):
        return f"<Author {self.name}>"

    def __str__(self):
        return f"Author: {self.name}, Born: {self.birth_date}, Died: {self.date_of_death}"


class Book(db.Model):
    __tablename__ = 'books'  # Optional: Specify the table name explicitly

    # Attributes
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-incrementing PK
    isbn = db.Column(db.String(13), unique=True, nullable=False)  # ISBN number (required, unique)
    title = db.Column(db.String(200), nullable=False)  # Title of the book (required)
    publication_year = db.Column(db.Integer, nullable=False)  # Publication year (required)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)  # Foreign Key to Author

    # Relationship
    author = db.relationship('Author', backref='books')  # Establish relationship with Author

    # String representation for debugging or display purposes
    def __repr__(self):
        return f"<Book {self.title} by {self.author.name}>"

    def __str__(self):
        return f"Book: {self.title}, ISBN: {self.isbn}, Published: {self.publication_year}, Author: {self.author.name}"

