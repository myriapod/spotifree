# classe serveur_BDD qui permet de communiquer avec la base de données mariadb spotifree créée par le BDD/main_bdd.py

import mariadb
import sys

class serveur_BDD():
    def __init__(self, user, password):
        self.conn = None
        self.cur = None
        # on utilise l'user et le password spotifree pour se connecter au serveur mariadb
        self.user = user
        self.password = password
        # on récupère les données du user à partir de la bdd
        self.user_data = None
        self.user_playlists = None
        self.user_friends = None
        self.user_id = None
    
    def deconnexion(self):
        # déconnexion au serveur mariadb
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
        # méthode qui vérifie si l'user existe déjà ou pas dans la BDD
        # besoin d'une connexion root pour accéder à la table users de la bdd (l'user n'y a pas les droits d'accès)
        self.connection_root()
        
        # on vérifie l'user et le password en même temps
        self.cur.execute(f'''SELECT * FROM users WHERE user_name LIKE "{self.user}" AND user_password LIKE "{self.password}" ''')
        self.user_data = self.cur.fetchall()
        
        if len(self.user_data) == 0 : 
            # si on ne trouve pas de résultat on renvoi false
            self.deconnexion() # deconnexion du root
            return False
        else:
            # sinon true
            self.deconnexion() # deconnexion du root
            return True
            
        
    
    def log_in(self):
        # après avoir fait un check_user on peut faire un log_in si il renvoit true
        # on récupère l'id de l'user à partir de la bdd users
        self.user_id = self.user_data[0][0]
        
        
        
    def sign_up(self):
        # si check_user renvoi false, on créer un utilisateur
        self.connection_root() # connexion au root pour accéder à la table users
        
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
        
        # rajoute l'user et son password dans la table users
        self.cur.execute(f"INSERT INTO users (user_name, user_password) VALUES ('{self.user}', '{self.password}')")
        # on récupère son id généré par l'auto-incrémentation
        self.cur.execute(f'''SELECT * FROM users WHERE user_name LIKE "{self.user}" AND user_password LIKE "{self.password}" ''')
        self.user_data = self.cur.fetchall()
        
        self.conn.commit()
        self.deconnexion()
        # définit self.user_id
        self.user_id = self.user_data[0][0]
    
    
    def connection_user(self):
        # méthode de connexion au serveur mariadb par l'username et password de spotifree
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
        # on récupère un curseur
        self.cur = self.conn.cursor()
        

    def get_user_data(self):
        # méthode qui affiche les données (playlists et friends) de l'user
        # plutôt utilisé dans la version ligne de commande de spotifree
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
        
        # pour récupérer le nom des amis, il faut passer par le root et la table users
        self.connection_root()
        friends = []
        for friend in self.user_friends:
            self.cur.execute(f'''SELECT user_name FROM users WHERE user_id = {friend[-1]}
                             ''')
            friends.append(self.cur.fetchall())
            
        print(f'{self.user}\'s Playlists: {self.user_playlists}\n{self.user}\'s Friends: {friends}')
        
    
    
    # recherche de musique dans la bdd
    def search(self, query):
        # cherche dans les noms d'artistes, les albums et les chansons sans différence
        self.cur.execute(f'''SELECT DISTINCT * FROM spotify WHERE artist_name LIKE "%{query}%" OR album_name LIKE "%{query}%" OR track_name LIKE "%{query}%"''')
        return self.cur.fetchall()
    
    
    
    # playlists
    def add_playlist(self, playlist_name, list_songs):
        # pas tout à fait abouti
        # on demande le nom de la playlist et la liste des chansons à partir de la recherche
        print('Adding a playlist')
        self.cur.execute(f"INSERT INTO playlists (owner_id, playlist_name, list_songs) VALUES ({self.user_id}, '{playlist_name}', '{list_songs}')")
        self.conn.commit()
        self.get_user_data()
            
    
    def show_playlists(self):
        # affiche les playlists de l'user s'il y en a
        if len(self.user_playlists)>0:
            return self.user_playlists
        else:
            print("Aucune playlist.")
        
        
        
    # spotifriends    
    def find_friend(self, friend_name):
        # recherche d'ami à partir du nom
        # connexion root pour vérifier son existence dans la table users
        self.connection_root()
        self.cur.execute(f'''SELECT * FROM users WHERE user_name LIKE "%{friend_name}%"''')
        results = self.cur.fetchall()
        self.deconnexion()
        self.connection_user()
        # s'il n'y a pas de résultats on renvoit none
        return None if len(results) == 0 else results
        
        
    def add_friends(self, amis_ids):
        print('Adding a friend') 
        # s'il y a déjà des amis qui existent, 
        if self.user_friends and len(self.user_friends)>0:
            friend_list = self.user_friends
            for friend in friend_list: # si l'ami des déjà présent dans la liste des amis
                if amis_ids == int(friend[1]):
                    print("Already befriended.")
                    return
            friend_list.append(amis_ids)
            # ajout dans la table amis
            self.cur.execute(f"INSERT INTO amis (user_id, amis_id) VALUES ({self.user_id}, '{friend_list[-1]}')")
        else: # si c'est le premier ami
            # ajout dans la table amis
            self.cur.execute(f"INSERT INTO amis (user_id, amis_id) VALUES ({self.user_id}, '{amis_ids}')")
        
        self.conn.commit()
        self.get_user_data()
        
        
    def show_friends(self):
        # affiche les amis dans le terminal s'il y en a
        if len(self.user_friends)>0 and self.user_friends[0][0]:
            print(self.user_friends)
        else:
            print("Aucun ami.")
        
    
