import mariadb
import sys

import spotipy # api spotify
from spotipy.oauth2 import SpotifyClientCredentials
import json
from requests.exceptions import ReadTimeout # pour gérer les erreurs de spopipy
from deepdiff import DeepDiff # pour vérifier qu'on ne rajoute pas plusieurs fois les mêmes chansons dans la bdd

# pour affichage terminal
LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'



### Partie mariadb ###
class BDD():
    def __init__(self, spotify_data=None):
        # déclaration de l'objet BDD qui a une connexion à mariadb, un curseur et une liste de données spotify
        self.conn = None
        self.cur = None
        self.spotify_data = spotify_data
    
    def deconnexion(self):
        # on commit les changements dans la bdd avant de se déconnecter
        self.conn.commit()
        self.conn.close()
        
    def connection_root(self):
        # Connect to MariaDB Platform avec le root pour pouvoir créer la BDD
        try:
            self.conn = mariadb.connect(
                user="root",
                password="123456", # à changer au besoin
                host="127.0.0.1",
                port=3306
            )
            
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Get Cursor
        self.cur = self.conn.cursor()
    
    def creation_bdd(self):
        # méthode de création de la bdd
        # on se connecte en root
        self.connection_root()
        
        # on supprime la database spotifree pour éviter les conflits
        # tant que le serveur flask ne ferme pas, la bdd reste ouverte et se met à jour
        self.cur.execute("DROP DATABASE spotifree")
        self.cur.execute("CREATE DATABASE IF NOT EXISTS spotifree")
        print(" > Created the database spotifree.") 
        
        # création de la table spotify
        self.cur.execute('''CREATE TABLE IF NOT EXISTS spotifree.spotify (
                        track_id INT UNIQUE PRIMARY KEY,
                        artist_name TEXT,
                        album_name TEXT,
                        track_name TEXT,
                        track_number INT,
                        spotify_link TEXT
                        )''')
        print(" > Created the table spotify.")
        
        # ajouter les données à la bdd spotify
        print(" > Filling the spotify table...")
        # pour chaque chanson de self.spotify_data
        for track in self.spotify_data:
            # on ajoute à la bdd l'id de la chanson, le nom de l'artiste, le nom de l'album, le nom de la chanson, le numéro de la chanson et le lien spotify
            self.cur.execute(f''' INSERT INTO spotifree.spotify (track_id, artist_name, album_name, track_name, track_number, spotify_link)
                         VALUES ({track['track_id']}, '{track['artist_name']}', '{track['album_name']}',
                                '{track['track_name']}', {track['track_number']}, '{track['spotify_link']}')
                         ''')
        print(LINE_UP, end=LINE_CLEAR) # affichage terminal plus propre
        print(" > Done filling the spotify table.")
        
        # création table users: user_id auto-incrémenté en primary key, user_name, user_password
        self.cur.execute('''CREATE TABLE IF NOT EXISTS spotifree.users (
                        user_id INT NOT NULL AUTO_INCREMENT,
                        user_name TEXT,
                        user_password TEXT,
                        PRIMARY KEY (user_id)
                        )''')
        print(" > Created the users table.")
        
        # création table playlsits: owner_id est un user_id, playlist_name et list_songs qui est un longtext (pas le meilleur format)
        self.cur.execute('''CREATE TABLE IF NOT EXISTS spotifree.playlists (
                        owner_id INT,
                        playlist_name TEXT,
                        list_songs LONGTEXT
                        )''')
        print(" > Created the playlists table.")
        
        # création table amis: user_id, amis_id (pas totalement abouti)
        self.cur.execute('''CREATE TABLE IF NOT EXISTS spotifree.amis (
                        user_id INT,
                        amis_id INT
                        )''')
        print(" > Created the amis table.")
        
        # deconnexion du root
        self.deconnexion()
        

        

### Partie Spotify ###

# on utilise l'api spotify spotipy (https://github.com/plamere/spotipy)
# permet de récupérer des dictionnaires à partir de requêtes de recherche envoyées à spotify
# doc: https://spotipy.readthedocs.io/en/2.19.0/ 


def connection_spotify():
    # credentials du projet spotifree données par spotify
    # https://developer.spotify.com/dashboard/applications/2bc3eddc577f4e4496d29334479f1780
    # avec le compte spotify de Solene
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="2bc3eddc577f4e4496d29334479f1780",
                                                           client_secret="174417f6ba92480789f1d88734a9c3e4"),
                           requests_timeout=10, retries=10) # timeout et retries pour éviter l'erreur timed out qui stoppait le programme


class Spotify_Artist():
    # définition d'un artiste spotify par son nom à chercher
    def __init__(self, artist):
        self.artist = artist
        sp = connection_spotify() # connection à l'api spotify
        try:
            # envoi de la requête à spotify, on limite les résultats à 5 artistes si la requête n'est pas assez précise
            self.results = sp.search(q=f"artist:{self.artist}", limit=5, type="artist")
        except ReadTimeout:
            print("Spotify timed out... trying again...")
            self.results = sp.search(q=f"artist:{self.artist}", limit=5, type="artist")
        
        # les résultats de la requête sont sous forme de dictionnaire
        # récupérer les données de l'artistes à partir des résultats
        items = self.results["artists"]["items"]
        if len(items) != 0: # s'il y a bien des résultats à la requête
            d = items[0]
        
        self.artist_ID = d["id"] # on récupère l'id spotify de l'artiste


class Spotify_Albums():
    # définition d'un album spotify à partir de l'id de son artiste
    def __init__(self, artist_id):
        sp = connection_spotify()
        try:
            # on affiche les 50 premiers albums (la plupart des artistes en ont moins que ça)
            self.results = sp.artist_albums(artist_id=artist_id, limit=50)
        except ReadTimeout:
            print("Spotify timed out... trying again...")
            self.results = sp.artist_albums(artist_id=artist_id, limit=50)
           
        self.album_ids = []
        self.album_names = []
        self.release_date = []
        self.total_tracks = []
        
        # on peut récupérer beaucoup de données intéressantes à partir de l'album, toutes ne sont pas utilisées dans ce programme
        albums = self.results['items']
        for album in albums:
            self.album_ids.append(album['id']) # on récupère l'id spotify de l'album
            self.album_names.append(album['name']) # on récupère le nom de l'album
            self.release_date.append(album['release_date']) # on récupère sa date de sortie (pas utilisé)
            self.total_tracks.append(album['total_tracks']) # on récupère le nombre total de tracks (pas utilisé)
        

class Spotify_Tracks():
    # définition d'une chanson spotify à partir de l'id de l'album
    def __init__(self, album_id, album_name, data, index):
        # on demande aussi le nom de l'album, la data totale et l'index pour permettre de faire l'ajout dans la spotify_bdd d'un coup
        sp = connection_spotify()
        try:
            # on affiche les 20 premières chansons d'un album (ce n'est peut être pas la totalité mais la bdd devient vite très grande)
            self.results = sp.album_tracks(album_id=album_id, limit=20)
        except ReadTimeout:
            print("Spotify timed out... trying again...")
            self.results = sp.album_tracks(album_id=album_id, limit=20)

        
        for track in self.results['items']:
            index.append(index[-1]+1) # un peu bizzare mais ça permet de donner un track_id unique
            # on ajoute directement à la liste de dictionnaire des chansons chaque chanson de l'album
            track_to_add = {'track_id' : index[-1],
                          # gérer l'erreur d'un ' en trop possible dans sql
                          'artist_name' : track['artists'][0]['name'].replace("\'", "\\'"), 
                          'album_name' : album_name.replace("\'", "\\'"),
                          'track_name' :  track['name'].replace("\'", "\\'"),
                          'track_number' : track['track_number'],
                          'spotify_link' : track['external_urls']['spotify']
                        }
            # on compare les dictionnaires déjà présents dans data avec la nouvelle chanson à rajouter pour éviter les doublons
            if len(data)==0:
                data.append(track_to_add)
            else:
                add = True
                for track in data:
                    diff = DeepDiff(track, track_to_add)
                    # compare deux dictionnaires entre eux et indique quelles valeurs sont différentes
                    if len(diff)>0:
                        list_keys = list(diff['values_changed'].keys())
                        if len(list_keys)==1:
                            # s'il y a plus d'une valeur différente (autre que l'id), ça veut dire que ce n'est pas la même chanson
                            add = False 
                            
                if add: # si c'est ok de rajouter la chanson à la bdd, on l'ajoute à la base de donnée data mise en entrée
                    data.append(track_to_add)
            
