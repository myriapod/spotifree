from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from sqlalchemy import select
from . import db
import json
import sys
sys.path.append("..")
from SERVEUR.classes_srv import serveur_BDD
import os

views = Blueprint('views', __name__)

# Une fois la connexion du user à son compte réussie -> redirection à la page home.html
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    try:
        stmt = db.select(User).where(User.first_name == current_user.first_name)
        result = db.session.execute(stmt)
        for user_obj in result.scalars():
            password = user_obj.password
        
        # Instanciation de la BDD par rapport à l'user 
        BDD = serveur_BDD(current_user.first_name, password)
        # On vérifie que l'user existe dans la table user 
        BDD.check_user()
        # Récupération du user id
        BDD.log_in()
        # Connexion à la BDD de l'user 
        BDD.connection_user()

        # Vérification s'il y a des amis dans la BDD amis
        friends = 0
        if BDD.user_friends:
            friends = BDD.user_friends

        # chercher les musiques
        if request.method == 'GET':
            # Récupère recherche de la musique
            recherche = request.args.get('recherche')
            # Récupère le nom d'un ami dans la barre de recherche
            friend_search = request.args.get('friend-search')
            
            # Cherche le nom d'un ami dans la BDD (si l'utilisateur existe ou pas)
            find_friend = BDD.find_friend(friend_search)
            # S'il trouve un ami, on récupère l'id de l'ami 
            if find_friend:
                friend_id = find_friend[0][0]
                # ajout id de l'ami dans la table ami de la BDD
                BDD.add_friends(friend_id)
            # Si on a quand même fait une recherche d'ami 
            elif friend_search:
                flash(f"Utilisateur {friend_search} non trouvé.")
        else:
            recherche = request.form.get('postTest')

        resultats = BDD.search(recherche)
        
        if request.method == 'POST':
            download_link = request.form['submit_button']
            try:
                flash('Musique en cours de téléchargement...')
                # le téléchargement se fait via os.system dans le terminal 
                os.system(f"spotdl {download_link}")
            except OSError as err:
                print(err)
            flash(f'Musique téléchargée.')
        
        return render_template("home.html", user=current_user, recherche=recherche, resultats=resultats, friends=friends,
                            friend_search=friend_search)

    # Première connexion -> redirection vers le login (erreur mariadb)
    except IndexError:
        return redirect(url_for('auth.login'))

