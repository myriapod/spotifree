from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    
    
class Music(db.Model):
    track_id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(150))
    album_name = db.Column(db.String(150))
    track_name = db.Column(db.String(150))
    track_number = db.Column(db.Integer)
    spotify_link = db.Column(db.String(150))

# Exemple de données musical.
# {
#     "track_id": 1,
#     "artist_name": "Artist Vs Poet",
#     "album_name": "Medicine",
#     "track_name": "Fresh",
#     "track_number": 1,
#     "spotify_link": "https://open.spotify.com/artist/3kYFawNQVZ00FQbgs4rVBe"
# }
