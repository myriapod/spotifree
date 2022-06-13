import mariadb
import sys
import json

# on récupère les données spotify depuis le json
with open('BDD/spotify_bdd.json', 'r') as input:
    spotify_data = json.load(f)


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
                password="123456",
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
        self.cur.execute('''CREATE TABLE IF NOT EXISTS spotifree.spotify (
                        track_id INT PRIMARY KEY,
                        artist_name TEXT,
                        album_name TEXT,
                        track_name TEXT,
                        track_number INT
                        )''')
        
        # ajouter les données à la bdd spotify
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS spotifree.users (
                        user_id INT PRIMARY KEY,
                        user_name TEXT,
                        user_password TEXT
                        )''')
        
        # les playlists sont des listes d'id de chanson
        self.cur.execute('''CREATE TABLE IF NOT EXISTS spotifree.playlists (
                        owner_id INT,
                        playlist_name TEXT,
                        list_songs TEXT,
                        FOREIGN KEY (owner_id) REFERENCES users(user_id)
                        )''')
        
        # liste d'id d'amis séparés par une virgule
        self.cur.execute('''CREATE TABLE IF NOT EXISTS spotifree.amis (
                        user_id INT,
                        amis_id TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                        )''')
        
        self.deconnexion()
        
    def connexion_user(self, user, password):
        self.connection_root()
        self.cur.execute(f"CREATE USER IF NOT EXISTS'{user}' IDENTIFIED BY '{password}'")
        
        # permissions particulières : https://mariadb.com/kb/en/grant/#table-privileges
        self.cur.execute(f"GRANT SELECT ON spotifree.spotify TO '{user}'@'localhost'")
        self.cur.execute(f"GRANT DELETE, INSERT ON spotifree.amis TO '{user}'@'localhost'")
        self.cur.execute(f"GRANT DELETE, INSERT ON spotifree.playlists TO '{user}'@'localhost'")
        # les utilisateurs n'ont pas accès à la base de donnée des users
        
        self.cur.execute("FLUSH PRIVILEGES")
        self.deconnexion()
        
    