from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Message
from . import db  
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home(): 
    return render_template("home.html", user=current_user)

@views.route('/about-us')
@login_required
def about():
    return render_template("about.html", user=current_user)

@views.route('/contact-us', methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        contact = request.form.get('contact') 

        message = Message.query.filter_by(contact=contact)
        if message:
        
            if len(contact) < 1:
                flash('You cannot send an empty message', category='error')
                return redirect(url_for('views.contact'))
            
            else:
                new_message = Message(contact=contact)
                db.create_all()
                db.session.add(new_message)
                db.session.commit()

            flash('Your message has been logged', category='success')

    return render_template("contact us.html", user=current_user)


