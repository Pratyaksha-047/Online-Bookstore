from main import app
from flask import render_template
#request
#from main import db

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route("/about")
def about():
    return render_template('about.html')




