from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User
from sqlalchemy import select
from . import db
import json
import sys
sys.path.append("..")
from spotifree.SERVEUR.classes_srv import serveur_BDD

views = Blueprint('views', __name__)

password = db.session.add(new_user)
BDD = serveur_BDD(current_user, "yy")

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    # chercher les musiques
    if request.method == 'GET':
        test2 = request.args.get('q')
    else:
        test2 = request.form.get('postTest')
    
    return render_template("home.html", user=current_user,test=test2)


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

