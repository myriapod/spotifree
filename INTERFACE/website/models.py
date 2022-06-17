# Classe User : permet de savoir sous quelle forme sont stockés les users inscrits dans la database.db (bdd user locale)
# La classe est rappelée lors du check pour la connexion au compte

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    
