from functools import wraps
from flask import abort
from flask_login import current_user
from flask import flash, redirect,url_for

def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash("You are not signed in as an admin")
            return redirect(url_for('home'))
        else:
            return function(*args, **kwargs)
    return wrapper