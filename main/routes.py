from main import app
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect,request
from main.forms import RegistrationForm, LoginForm , ContactForm , UpdateAccountForm,ResetPasswordForm, Add_bookForm, RequestResetForm, ForgotPasswordForm
from main.models import Book, User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flask_admin.contrib.sqla import ModelView
from main.decorators import admin_required
from main import db, bcrypt,mail, admin
import razorpay

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        msg = Message("Feedback for Online Bookstore Management Website",
            sender="decodemysteries2021@gmail.com",
            recipients=["receiver1@gmail.com","receiver2@gmail.com"])

        msg.body = '''Hey developers,
        A Client just viewed your website. The Details of feedback are:
                  
        Name of client: %s
        Email address: %s
        Feedback from client: %s
        '''%(form.name.data,form.email.data,form.feedback.data)
        mail.send(msg)
        return redirect(url_for('home'))

    return render_template('contact.html',title='Contact',form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, phone=form.phone.data, address=form.address.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/admin", methods=['GET', 'POST'])
@login_required
@admin_required
def adminfunc():
    pass
class myModelView(ModelView):
    edit_template = 'edit_user.html'
    create_template = 'create_user.html'
    list_template = 'list_user.html'
    def is_accessible(self):
        return (current_user.is_admin==True)
    
admin.add_view(myModelView(User,db.session))
admin.add_view(myModelView(Book,db.session))

@app.route("/add_book", methods=['GET', 'POST'])
@login_required
@admin_required
def add_book():
    form= Add_bookForm() 
    if form.validate_on_submit():
        image_f = save_picture(form.image_file.data)
        book = Book(title=form.title.data, author=form.author.data, publishing_year=form.publishing_year.data, genre=form.genre.data, nocopies=form.nocopies.data,description=form.description.data,image_file=image_f, price=form.price.data)
        db.session.add(book)
        db.session.commit()
        flash('A book has been added to the collection!', 'success')
        return redirect(url_for('add_book'))
    return render_template('add_book.html',title='Add_book', form=form)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form1 = UpdateAccountForm()
    form2 = ResetPasswordForm()
    if form1.validate_on_submit():
        current_user.name = form1.name.data
        current_user.phone = form1.phone.data
        current_user.address = form1.address.data
        current_user.email = form1.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form1.name.data = current_user.name
        form1.email.data = current_user.email
        form1.phone.data = current_user.phone
        form1.address.data = current_user.address
        
    if form2.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form2.old_password.data):
            current_user.password = bcrypt.generate_password_hash(form2.new_password.data).decode('utf-8')
            db.session.commit()
            flash('Password Changed', 'Success')
            return redirect(url_for('account'))
        else:
            flash('Old Password not changed', 'danger')
        
    return render_template('account.html', title='Account', account_form=form1, password_form =form2)

'''def image():
    image_file = url_for('static/img',filename='books/'+)'''
    
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static\\img\\books', picture_fn)

    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/book", methods=['GET', 'POST'])
def book():
    q= request.args.get('q')
    if q:
        books = Book.query.filter(Book.title.contains(q) |
        Book.author.contains(q))
    else:
        books=Book.query.all()
    return render_template('book.html', books=books)

@app.route("/book_info/<int:book_id>")
def book_info(book_id):
    book = Book.query.get_or_404(book_id)
    client = razorpay.Client(auth=("rzp_test_OPH3Y9PSTTXz6z","n19uDbf0UQdIuBFILCrVKyiC"))
    payment = client.order.create({'amount': book.price*100 , 'currency' : "INR" , "payment_capture": '1'})
    db.session.commit()
    
        
    return render_template('book_info.html', title=book.title, book=book , payment=payment)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
