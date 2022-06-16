from classes_srv import serveur_BDD
import os

def connection():
    print('----LOGIN TO SPOTIFREE----')
    user = input("Username: ")
    password = input("Password: ")
    print('-------------------------')
    return user, password

def search(bdd, query):
    print("Searching query")
    return bdd.search(query)

def display_result(results):
    if len(results)>10: # s'il y a plus de 10 résultats
        print(f"Showing 10 results out of {len(results)} total results.")
        for index in range(1, 11): # on montre que les 10 premiers résultats
            print(f'{index} > {results[index-1][1]} - {results[index-1][2]} - {results[index-1][3]}')
            
    elif len(results)>0: # s'il y a moins que 10 résultats mais quand même des résultats
        index = 1
        while index < len(results)+1 : # on montre que les 10 premiers résultats
            print(f'{index} > {results[index-1][1]} - {results[index-1][2]} - {results[index-1][3]}')
            # artiste, album, titre chanson
            index += 1
        print(f"Showing {index-1} results.")
    else:
        print('Aucun résultat')
        return
            
def select_song(results):
    selection = int(input("Selection de la chanson (numéro du résultat): "))
    print(f'Chanson choisie: {results[selection-1][1]} - {results[selection-1][2]} - {results[selection-1][3]}')
    return selection

def menu(bdd):
    print('\n\n------------MENU---------')
    print('1. Search\n2. Playlists\n3. Friends')
    print('-------------------------')
    choice = int(input('Entrez numéro: '))
    if choice == 1:
        # affiche les résultats mais pas moyen de sélectionner ce qu'on veut
        query = input("Recherche: ")
        results = search(bdd, query)
        display_result(results)            
        selection = select_song(results)
        print("Lancement du téléchargement...")
        try:
            os.system(f"spotdl {results[selection-1][5]}")
        except OSError as err:
            print()

    elif choice == 2:
        bdd.show_playlists()
        choice = input("Create new playlist? (Y/N)")
        if choice in ["yes", "Yes", "oui", "Oui", "o", "y"]:
            print("New playlist!")
            playlist_name = input("Nom de la playlist: ")
            
            print("Sélectionner des chansons:")

            playlist_selection = []
            
            more=True
            while more:
                # besoin de trouver comment sélectionner une chanson et en tirer son id
                query = input("Recherche chanson: ")
                results = search(bdd, query)
                display_result(results)
                playlist_selection.append(select_song(results))
                choice = input("Autre recherche?")
                if choice not in ["yes", "Yes", "oui", "Oui", "o", "y"]:
                    more=False
                    
            print("Ajout dans la playlist...")
            bdd.add_playlist(playlist_name=playlist_name, list_songs=playlist_selection)

    elif choice == 3:
        # on a accès que aux ids, il faudrait refaire une connection root pour afficher les usernames à partir des id
        bdd.show_friends() 

        # ajouter des amis marche
        choice = input("Want a new friend? (Y/N)")
        if choice in ["yes", "Yes", "oui", "Oui", "o", "y"]:
            friend_name = input("New friend name: ")
            friend_result = bdd.find_friend(friend_name)
            if friend_result:
                friend_id = friend_result[0][0]
                bdd.add_friends(friend_id)
            else:
                print("Couldn't find this friend.")
        


def main():
    # start mariadb
    # os.system("sudo systemctl restart mariadb") 
    # demande le mdp sudo, pas top

    while True:
        try:
            user, password = connection()
            break
        except Exception:
            print('User exists. Wrong password.')
            user, password = connection()
            
    spotifree = serveur_BDD(user, password)
    if not spotifree.check_user():
        spotifree.sign_up()
    else:
        spotifree.log_in()

    spotifree.connection_user()
    
    os.system("clear")
    spotifree.get_user_data()

    while True:
        try:
            menu(spotifree)
        except KeyboardInterrupt:
            print("Closing.")
            break


    # spotifree.get_user_data()
    spotifree.deconnexion()
    
main()