from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import sys
sys.path.append("..")
from spotifree.SERVEUR.classes_srv import serveur_BDD


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        flask_user = User.query.filter_by(first_name=username).first()
        
        BDD = serveur_BDD(username, password)
        exists = BDD.check_user()
        
        if exists and flask_user:
            flash('Logged in successfully!', category='success')
            login_user(flask_user, remember=True)
            return redirect(url_for('views.home'))
            #if check_password_hash(user.password, password):
            #    flash('Logged in successfully!', category='success')
            #    login_user(user, remember=True)
            #    return redirect(url_for('views.home'))
            #else:
            #    flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist or error with password.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        flask_user = User.query.filter_by(first_name=first_name).first()

        BDD = serveur_BDD(first_name, password1)
        exists = BDD.check_user()
        
        if exists:
            flash('Username already exists.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            BDD.sign_up()
            # on crée l'utilisateur sur une bdd locale pour pouvoir utiliser login_user de flask
            new_user = User(first_name=first_name, password=password1)
            # avec le mdp crypté:
            # new_user = User(first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)
