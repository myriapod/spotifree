from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User
from sqlalchemy import select
from . import db
import json
import sys
sys.path.append("..")
from spotifree.SERVEUR.classes_srv import serveur_BDD
import os

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    stmt = db.select(User).where(User.first_name == current_user.first_name)
    result = db.session.execute(stmt)
    for user_obj in result.scalars():
        password = user_obj.password
    
    BDD = serveur_BDD(current_user.first_name, password)
    BDD.connection_user()

    # chercher les musiques
    if request.method == 'GET':
        recherche = request.args.get('q')
    else:
        recherche = request.form.get('postTest')
        
    resultats = BDD.search(recherche)
    
    if request.method == 'POST':
        download_link = request.form['submit_button']
        try:
            os.system(f"spotdl {download_link}")
        except OSError as err:
            print()
    
    return render_template("home.html", user=current_user,recherche=recherche, resultats=resultats)


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

