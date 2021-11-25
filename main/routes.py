from main import app
from flask import render_template, url_for, flash, redirect,request
from main.forms import RegistrationForm, LoginForm , ContactForm , UpdateAccountForm,ResetPasswordForm
from main.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
#request
from main import db, bcrypt,mail

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
