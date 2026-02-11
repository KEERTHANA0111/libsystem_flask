import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Admin, Member, Book, Borrow, RequestForBooks, BookStatus, BorrowStatus, PositionEnum
from datetime import datetime
from extensions import db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')
# Default to SQLite for ease of setup, but configurable via environment
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///library.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        if '_' not in user_id:
            return None
        role, uid = user_id.split('_')
        if role == 'admin':
            return Admin.query.get(int(uid))
        return Member.query.get(int(uid))
    except Exception:
        return None

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/')
def index():
    if current_user.is_authenticated:
        if isinstance(current_user, Admin):
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('member_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        user = None
        if role == 'admin':
            user = Admin.query.filter_by(username=username).first()
        else:
            user = Member.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f'Welcome back, {user.firstName}!', 'success')
            return redirect(url_for('admin_dashboard' if role == 'admin' else 'member_dashboard'))
        
        flash('Invalid username, password, or role selection.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        position = request.form.get('position')
        
        if Member.query.filter_by(username=username).first() or Admin.query.filter_by(username=username).first():
            flash('Username already exists', 'warning')
            return redirect(url_for('register'))
            
        new_member = Member(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            firstName=first_name,
            lastName=last_name,
            position=PositionEnum(position) if position else PositionEnum.STUDENT
        )
        db.session.add(new_member)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not isinstance(current_user, Admin):
        flash("Unauthorized access.", "danger")
        return redirect(url_for('member_dashboard'))
        
    stats = {
        'total_books': Book.query.count(),
        'issued_books': Book.query.filter_by(status=BookStatus.ISSUED).count(),
        'requests': RequestForBooks.query.count(),
        'total_members': Member.query.count()
    }
    books = Book.query.all()
    # For the issue book dropdown
    members = Member.query.all()
    return render_template('admin_dash.html', stats=stats, books=books, members=members)

@app.route('/admin/inventory', methods=['POST'])
@login_required
def add_inventory():
    if not isinstance(current_user, Admin):
        return redirect(url_for('index'))
        
    title = request.form.get('title')
    author = request.form.get('author')
    price = request.form.get('price')
    publisher = request.form.get('publisher')
    
    if not title:
        flash('Title is required', 'danger')
        return redirect(url_for('admin_dashboard'))

    new_book = Book(
        title=title, 
        author=author, 
        price=float(price) if price else 0.0, 
        publisher=publisher
    )
    db.session.add(new_book)
    db.session.commit()
    flash('Book Added Successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/issue', methods=['POST'])
@login_required
def issue_book():
    if not isinstance(current_user, Admin):
        return redirect(url_for('index'))
        
    book_id = request.form.get('book_id')
    member_id = request.form.get('member_id')
    
    book = Book.query.get(book_id)
    member = Member.query.get(member_id)
    
    if book and member and book.status == BookStatus.AVAILABLE:
        borrow = Borrow(book_id=book_id, member_id=member_id)
        book.status = BookStatus.ISSUED
        db.session.add(borrow)
        db.session.commit()
        flash(f'Book "{book.title}" issued to {member.firstName}', 'success')
    else:
        flash('Unable to issue book. Check if book is available.', 'danger')
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/return/<int:borrow_id>', methods=['POST'])
@login_required
def return_book(borrow_id):
    if not isinstance(current_user, Admin):
        return redirect(url_for('index'))
        
    borrow = Borrow.query.get_or_404(borrow_id)
    book = Book.query.get(borrow.book_id)
    
    borrow.status = BorrowStatus.RETURNED
    borrow.return_date = datetime.utcnow()
    book.status = BookStatus.AVAILABLE
    
    db.session.commit()
    flash(f'Book "{book.title}" has been returned.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/member/dashboard')
@login_required
def member_dashboard():
    if isinstance(current_user, Admin):
        return redirect(url_for('admin_dashboard'))
    
    my_borrows = Borrow.query.filter_by(member_id=current_user.id).all()
    return render_template('member_dash.html', borrows=my_borrows)

@app.route('/member/search')
@login_required
def search_books():
    query = request.args.get('q', '')
    if query:
        results = Book.query.filter(
            (Book.title.ilike(f"%{query}%")) | 
            (Book.author.ilike(f"%{query}%")) |
            (Book.publisher.ilike(f"%{query}%"))
        ).all()
    else:
        results = Book.query.all()
    return render_template('search_books.html', results=results, query=query)

@app.route('/member/request', methods=['POST'])
@login_required
def request_book():
    book_name = request.form.get('bookName')
    author_name = request.form.get('authorName')
    description = request.form.get('description')
    
    new_request = RequestForBooks(
        bookName=book_name,
        authorName=author_name,
        description=description
    )
    db.session.add(new_request)
    db.session.commit()
    flash('Your request has been submitted to the admin.', 'info')
    return redirect(url_for('member_dashboard'))

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Seed an admin if none exists
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(
                username='admin',
                password_hash=generate_password_hash('password123'),
                firstName='System',
                lastName='Admin',
                email='admin@library.com'
            )
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: admin / password123")
            
    app.run(debug=True, port=5000)
