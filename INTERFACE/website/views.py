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


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    try:
        stmt = db.select(User).where(User.first_name == current_user.first_name)
        result = db.session.execute(stmt)
        for user_obj in result.scalars():
            password = user_obj.password
        
        BDD = serveur_BDD(current_user.first_name, password)
        BDD.check_user()
        BDD.log_in()
        BDD.connection_user()
    
        friends = 0
        if BDD.user_friends:
            friends = BDD.user_friends

        # chercher les musiques
        if request.method == 'GET':
            recherche = request.args.get('recherche')
            friend_search = request.args.get('friend-search')
            
            find_friend = BDD.find_friend(friend_search)
            if find_friend:
                friend_id = find_friend[0][0]
                BDD.add_friends(friend_id)
            elif friend_search:
                flash(f"Utilisateur {friend_search} non trouvé.")
        else:
            recherche = request.form.get('postTest')

        resultats = BDD.search(recherche)
        
        if request.method == 'POST':
            download_link = request.form['submit_button']
            try:
                flash('Musique en cours de téléchargement...')
                os.system(f"spotdl {download_link}")
            except OSError as err:
                print(err)
            flash(f'Musique téléchargée.')
        
        return render_template("home.html", user=current_user, recherche=recherche, resultats=resultats, friends=friends,
                            friend_search=friend_search)

    except IndexError:
        return redirect(url_for('auth.login'))

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})

