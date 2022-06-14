import mariadb
import sys

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

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
        
    