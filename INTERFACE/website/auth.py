# Script permettant l'inscription, la connexion et la déconnexion à Spotifree

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import sys
sys.path.append("..")
from SERVEUR.classes_srv import serveur_BDD


auth = Blueprint('auth', __name__)

# Fonction permettant de se connecter au compte Spotifree
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Récupération de l'username et du password tapés sur la page
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check avec le username stocké dans la BDD locale (faite avec flask : database.db) lors de l'inscription
        flask_user = User.query.filter_by(first_name=username).first()
        
        # Import de la BDD user mariadb et check si l'user existe également
        BDD = serveur_BDD(username, password)
        exists = BDD.check_user()
        
        # Si les deux checks sont concluants -> succès de connexion et redirection à la page home.html
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
            
        # Sinon -> erreur, pas de connexion
        else:
            flash('User does not exist or error with password.', category='error')

    return render_template("login.html", user=current_user)

# Fonction déconnexion
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Fonction sign_up pour faire inscrire un compte à Spotifree
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # On récupère le nom, le mot de passe et la confirmation du mot de passe (password2) et stockage dans bdd user locale (flask) et bdd user mariadb
        first_name = request.form.get('firstName') 
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        flask_user = User.query.filter_by(first_name=first_name).first()

        BDD = serveur_BDD(first_name, password1)
        exists = BDD.check_user()
        
        # Si le nom d'utilisateur rentré existe déjà -> erreur
        if exists:
            flash('Username already exists.', category='error')
        # Nom utilisateur doit avoir plus de 2 caractères
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        # si password1 différent de password2 -> erreur
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        # password doit avoir plus de 7 caractères
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        # Si conditions sont remplies -> création d'un nouveau compte
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
