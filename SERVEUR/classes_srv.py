import mariadb
import sys

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

class serveur_BDD():
    def __init__(self, user, password):
        self.conn = None
        self.cur = None
        self.user = user
        self.password = password
        self.user_data = None
        self.user_playlists = None
        self.user_friends = None
        self.user_id = None
    
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
                port=3306,
                database="spotifree"
            )
            
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Get Cursor
        self.cur = self.conn.cursor()
    
    def check_user(self):
        self.connection_root()
        
        self.cur.execute(f'''SELECT * FROM users WHERE user_name LIKE "{self.user}" AND user_password LIKE "{self.password}" ''')
        self.user_data = self.cur.fetchall()
        
        if len(self.user_data) == 0 : 
            self.deconnexion()
            return False
        else:
            self.deconnexion()
            return True
            
        
    
    def log_in(self):
        self.user_id = self.user_data[0][0]
        
        
        
    def sign_up(self):
        self.connection_root()
        
        self.cur.execute(f"CREATE USER IF NOT EXISTS '{self.user}'@'localhost' IDENTIFIED BY '{self.password}'")
        
        self.cur.execute("FLUSH PRIVILEGES")
        
        # permissions particulières : https://mariadb.com/kb/en/grant/#table-privileges
        # les users ne son't pas dans l'hote localhost mais dans l'hote %
        self.cur.execute(f"GRANT USAGE ON *.* TO '{self.user}'@'localhost'")
        self.cur.execute(f"GRANT SELECT ON spotify TO '{self.user}'@'localhost'")
        self.cur.execute(f"GRANT SELECT, DELETE, INSERT ON amis TO '{self.user}'@'localhost'")
        self.cur.execute(f"GRANT SELECT, DELETE, INSERT ON playlists TO '{self.user}'@'localhost'")
        # les utilisateurs n'ont pas accès à la base de donnée des users
        
        self.cur.execute("FLUSH PRIVILEGES")
        
        # marche pas très bien? ça rentre pas en vrai dans la database mais jsp pas pourquoi
        self.cur.execute(f"INSERT INTO users (user_name, user_password) VALUES ('{self.user}', '{self.password}')")
        self.cur.execute(f'''SELECT * FROM users WHERE user_name LIKE "{self.user}" AND user_password LIKE "{self.password}" ''')
        self.user_data = self.cur.fetchall()
        
        self.conn.commit()
        self.deconnexion()
        self.user_id = self.user_data[0][0]
    
    
    def connection_user(self):
        try:
            self.conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host="127.0.0.1",
                port=3306,
                database="spotifree"
                )
            # print("Connected to medicaments")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.cur = self.conn.cursor()
        

    def get_user_data(self):
        print(f'{self.user}\'s Profile:')
        self.cur.execute(f'''                         
                         SELECT *
                         FROM playlists 
                         WHERE playlists.owner_id={self.user_id}''')
        playlists = self.cur.fetchall()
        self.cur.execute(f'''                         
                         SELECT *
                         FROM amis 
                         WHERE amis.user_id={self.user_id}''')
        amis = self.cur.fetchall()
        
        # if len(playlists)>0:
        self.user_playlists = playlists
        # elif len(amis)>0:
        self.user_friends = amis
        
        self.connection_root()
        friends = []
        for friend in self.user_friends:
            self.cur.execute(f'''SELECT user_name FROM users WHERE user_id = {friend[-1]}
                             ''')
            friends.append(self.cur.fetchall())
            
        print(f'{self.user}\'s Playlists: {self.user_playlists}\n{self.user}\'s Friends: {friends}')
        
    
    
    # recherche
    def search(self, query):
        self.cur.execute(f'''SELECT DISTINCT * FROM spotify WHERE artist_name LIKE "%{query}%" OR album_name LIKE "%{query}%" OR track_name LIKE "%{query}%"''')
        return self.cur.fetchall()
    
    
    
    # playlists
    def add_playlist(self, playlist_name, list_songs):
        print('Adding a playlist')
        self.cur.execute(f"INSERT INTO playlists (owner_id, playlist_name, list_songs) VALUES ({self.user_id}, '{playlist_name}', '{list_songs}')")
        self.conn.commit()
        self.get_user_data()
            
    
    def show_playlists(self):
        if len(self.user_playlists)>0:
            return self.user_playlists
        else:
            print("Aucune playlist.")
        
        
        
    # spotifriends    
    def find_friend(self, friend_name):
        self.connection_root()
        self.cur.execute(f'''SELECT * FROM users WHERE user_name LIKE "%{friend_name}%"''')
        results = self.cur.fetchall()
        self.deconnexion()
        self.connection_user()
        return None if len(results) == 0 else results
        
        
    def add_friends(self, amis_ids):
        print('Adding a friend') 
        # need to add to the previous list of friends and check that it's not already there
        if self.user_friends and len(self.user_friends)>0:
            friend_list = self.user_friends
            for friend in friend_list:
                if amis_ids == int(friend[1]):
                    print("Already befriended.")
                    return
            friend_list.append(amis_ids)
            self.cur.execute(f"INSERT INTO amis (user_id, amis_id) VALUES ({self.user_id}, '{friend_list[-1]}')")
        else: # si c'est le premier ami
            print(self.user_id, amis_ids)
            self.cur.execute(f"INSERT INTO amis (user_id, amis_id) VALUES ({self.user_id}, '{amis_ids}')")
        
        self.conn.commit()
        self.get_user_data()
        
        
    def show_friends(self):
        if len(self.user_friends)>0 and self.user_friends[0][0]:
            print(self.user_friends)
        else:
            print("Aucun ami.")
        
    