from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        passwordx = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if  (passwordx == user.password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
                
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        lastname = request.form.get('lastname')
        firstname = request.form.get('firstname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        sub1 = "@"
        sub2 = "."

        if len(lastname) < 1:
            flash("Please, input your lastname", category="error")
        elif len(firstname) < 1:
            flash("Please, input your firstname", category="error")
        elif sub1 not in email or sub2 not in email:
            flash("Email not valid", category="error")
        elif len(phone) < 11:
            flash("Phone number not valid", category="error")
        elif len(password) < 1:
            flash("Please, input your password", category="error")
        elif len(password2) < 1:
            flash("Please, confirm your password", category="error")
        elif password != password2:
            flash("Passwords do not match", category="error")
        else:
  
            new_user = User(lastname=lastname, firstname=firstname,
                  email=email, phone=phone, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Succesfully created!', category='success')
            return redirect(url_for('auth.login'))
    return render_template("signup.html", user=current_user)

@auth.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)