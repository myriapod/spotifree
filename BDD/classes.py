import mariadb
import sys

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from requests.exceptions import ReadTimeout # pour gérer les erreurs de spopipy

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

### Partie mariadb ###
class BDD():
    def __init__(self, spotify_data):
        self.conn = None
        self.cur = None
        self.spotify_data = spotify_data
    
    def deconnexion(self):
        self.conn.close()
        
    def connection_root(self):
        # Connect to MariaDB Platform
        try:
            self.conn = mariadb.connect(
                user="root",
                password="123456", # à changer au besoin
                # dans le docker: installer mariadb et créer l'utilisateur root avec ce pswd
                host="127.0.0.1",
                port=3306
            )
            
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Get Cursor
        self.cur = self.conn.cursor()
    
    def creation_bdd(self):
        self.connection_root()
        
        self.cur.execute("CREATE DATABASE IF NOT EXISTS spotifree")
        print(" > Created the database spotifree.")
        
        self.cur.execute("DROP TABLE spotifree.spotify")
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
        for track in self.spotify_data:
            self.cur.execute(f''' INSERT INTO spotifree.spotify (track_id, artist_name, album_name, track_name, track_number, spotify_link)
                         VALUES ({track['track_id']}, '{track['artist_name']}', '{track['album_name']}',
                                '{track['track_name']}', {track['track_number']}, '{track['spotify_link']}')
                         ''')
        print(LINE_UP, end=LINE_CLEAR)
        print(" > Done filling the spotify table.")
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS spotifree.users (
                        user_id INT PRIMARY KEY,
                        user_name TEXT,
                        user_password TEXT
                        )''')
        print(" > Created the users table.")
        
        # les playlists sont des listes d'id de chanson
        self.cur.execute('''CREATE TABLE IF NOT EXISTS spotifree.playlists (
                        owner_id INT,
                        playlist_name TEXT,
                        list_songs TEXT,
                        FOREIGN KEY (owner_id) REFERENCES users(user_id)
                        )''')
        print(" > Created the playlists table.")
        
        # liste d'id d'amis séparés par une virgule
        self.cur.execute('''CREATE TABLE IF NOT EXISTS spotifree.amis (
                        user_id INT,
                        amis_id TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                        )''')
        print(" > Created the amis table.")
        
        self.deconnexion()
        
    def creation_user(self, user, password):
        self.connection_root()
        self.cur.execute(f"CREATE USER IF NOT EXISTS '{user}' IDENTIFIED BY '{password}'")
        
        self.cur.execute("FLUSH PRIVILEGES")
        
        # self.cur.execute(f'select user, host from mysql.user')
        # results = self.cur.fetchall()
        # for r in results:
        #    print(r)
        
        # permissions particulières : https://mariadb.com/kb/en/grant/#table-privileges
        # les users ne son't pas dans l'hote localhost mais dans l'hote %
        self.cur.execute(f"GRANT USAGE ON spotifree.* TO '{user}'@'%'")
        self.cur.execute(f"GRANT SELECT ON spotifree.spotify TO '{user}'@'%'")
        self.cur.execute(f"GRANT SELECT, DELETE, INSERT ON spotifree.amis TO '{user}'@'%'")
        self.cur.execute(f"GRANT SELECT, DELETE, INSERT ON spotifree.playlists TO '{user}'@'%'")
        # les utilisateurs n'ont pas accès à la base de donnée des users
        
        self.cur.execute("FLUSH PRIVILEGES")
        self.deconnexion()
        

### Partie Spotify ###

# creation de la bdd pour un utilisateur en lui donnant des identifiants mariadb

# https://github.com/plamere/spotipy 
# doc: https://spotipy.readthedocs.io/en/2.19.0/ 


def connection_spotify():
    # credentials du projet spotifree
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="2bc3eddc577f4e4496d29334479f1780",
                                                           client_secret="174417f6ba92480789f1d88734a9c3e4"),
                           requests_timeout=10, retries=10) # timeout et retries pour éviter l'erreur timed out


class Spotify_Artist():
    def __init__(self, artist):
        sp = connection_spotify()
        try:
            self.results = sp.search(q=artist, limit=20, type="artist") # on cherche les 20 premiers résultats qui correspondent au nom de l'artiste
        except ReadTimeout:
            print("Spotify timed out... trying again...")
            self.results = sp.search(q=artist, limit=20, type="artist")
            
        items = self.results["artists"]["items"]
        if len(items) != 0:
            d = items[0]

        self.artist_ID = d["id"] # on récupère l'id spotify de l'artiste


class Spotify_Albums():
    def __init__(self, artist_id):
        sp = connection_spotify()
        try:
            self.results = sp.artist_albums(artist_id=artist_id, limit=50) # à partir de l'id de l'artiste on peut afficher ses 50 premiers albums
        except ReadTimeout:
            print("Spotify timed out... trying again...")
            self.results = sp.artist_albums(artist_id=artist_id, limit=50)
            
        self.album_ids = []
        self.album_names = []
        self.release_date = []
        self.total_tracks = []
        
        albums = self.results['items']
        for album in albums:
            self.album_ids.append(album['id']) # on récupère l'id spotify de l'album
            self.album_names.append(album['name']) # on récupère le nom de l'album
            self.release_date.append(album['release_date']) # on récupère sa date de sortie (pas utilisé)
            self.total_tracks.append(album['total_tracks']) # on récupère le nombre total de tracks (pas utilisé)
        

class Spotify_Tracks():
    def __init__(self, album_id, album_name, data, index):
        sp = connection_spotify()
        try:
            self.results = sp.album_tracks(album_id=album_id, limit=20) # à partir de l'id de l'album, on peut afficher les 20 premières chansons dedans
        except ReadTimeout:
            print("Spotify timed out... trying again...")
            self.results = sp.album_tracks(album_id=album_id, limit=20)

        
        for track in self.results['items']:
            index.append(index[-1]+1) # un peu bizzare mais ça permet de donner un track_id unique
            # on ajoute directement à la liste de dictionnaire des chansons chaque chanson de l'album
            data.append({'track_id' : index[-1],
                          # gérer l'erreur d'un ' en trop possible dans sql
                          'artist_name' : track['artists'][0]['name'].replace("\'", "\\'"), 
                          'album_name' : album_name.replace("\'", "\\'"),
                          'track_name' :  track['name'].replace("\'", "\\'"),
                          'track_number' : track['track_number'],
                          'spotify_link' : track['artists'][0]['external_urls']['spotify']
                        })
            