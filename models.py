from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import enum
from extensions import db


class PositionEnum(enum.Enum):
    STUDENT = "STUDENT"
    FACULTY = "FACULTY"

class BookStatus(enum.Enum):
    AVAILABLE = "AVAILABLE"
    ISSUED = "ISSUED"

class BorrowStatus(enum.Enum):
    BORROWED = "BORROWED"
    RETURNED = "RETURNED"

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    mobile = db.Column(db.String(15))
    email = db.Column(db.String(100))
    pic = db.Column(db.String(255), default="https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=crop&q=80&w=200")
    
    def get_id(self):
        return f"admin_{self.id}"

class Member(db.Model, UserMixin):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    position = db.Column(db.Enum(PositionEnum), default=PositionEnum.STUDENT)
    mobile = db.Column(db.String(15))
    email = db.Column(db.String(100))
    pic = db.Column(db.String(255), default="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&q=80&w=200")

    def get_id(self):
        return f"member_{self.id}"

class Book(db.Model):
    __tablename__ = 'books'
    bookId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    price = db.Column(db.Float)
    publisher = db.Column(db.String(100))
    status = db.Column(db.Enum(BookStatus), default=BookStatus.AVAILABLE)

class Borrow(db.Model):
    __tablename__ = 'borrow'
    borrow_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.bookId'))
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.Enum(BorrowStatus), default=BorrowStatus.BORROWED)
    proof_pic = db.Column(db.String(255))
    
    # Relationships
    book = db.relationship('Book', backref='borrows')
    member = db.relationship('Member', backref='borrows')

class RequestForBooks(db.Model):
    __tablename__ = 'requestforbooks'
    requestId = db.Column(db.Integer, primary_key=True)
    bookName = db.Column(db.String(200))
    authorName = db.Column(db.String(100))
    description = db.Column(db.Text)
    requestDate = db.Column(db.DateTime, default=datetime.utcnow)
