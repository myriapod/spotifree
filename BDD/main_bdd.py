from BDD.classes import BDD, Spotify_Artist, Spotify_Albums, Spotify_Tracks
import json
import os

# pour l'affichage terminal
LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'



##############  DONNEES SPOTIFY  ##############

def spotify_donnees():
    # récupération des données de chansons à partir de l'api spotify
    
    # liste du nom des chanteurs et groupes à chercher sur spotify
    # on peut en rajouter autant qu'on veut, mais les requêtes internet prennent un certain temps
    list_artists = ['rihannah', 'coldplay', 'eminem', 'seventeen', 'monsta x', 'loona']


    index = [0] # numéro de la chanson rajoutée (est incrémentée par la classe Spotify_Tracks
    spotify_data = [] # initialisation de la liste qui contiendra tous les dictionnaires des chansons
    print("Extracting data from spotify\n")
    for artist in list_artists:
        # pour chaque artiste dans la liste des artistes à rechercher
        print(LINE_UP, end=LINE_CLEAR)
        print(f" > Working on {artist}...") # affichage terminal pour tracker le progrés
        
        # création de l'objet artist à partir du nom de l'artiste
        artist = Spotify_Artist(artist)
        
        # création de l'objet album à partir de l'id de l'objet artist
        album = Spotify_Albums(artist.artist_ID)
        
        # on parcours la longueur de la liste album_ids de l'objet album qui définit le nombre de chansons dans l'album
        for i in range(len(album.album_ids)):
            # création de l'object tracks à partir de l'id de l'album et de l'id de la chanson
            # Spotify_Tracks rajoute les chansons dans spotify_data
            # et incrémente index
            tracks = Spotify_Tracks(album.album_ids[i], album.album_names[i], spotify_data, index)
            
    # pour optimiser le temps de calcul :
    # on rajoute un file json pour garder en mémoire les données sans devoir extraire à nouveau d'internet
    with open('BDD/spotify_bdd.json', 'w') as output_file:
        json.dump(spotify_data, output_file)
    
    # affichage terminal de complétion
    print(LINE_UP, end=LINE_CLEAR)
    print("Spotify data collected.")



###################  BDD  #########################

def bdd():
    # création de la bdd mariadb
    
    # on récupère les données des chansons stockées dans le spotify_bdd.json
    with open('BDD/spotify_bdd.json', 'r') as input_file:
        spotify_data = json.load(input_file)
    # print(spotify_data)

    # création de la bdd spotifree et des tables users, spotify, playlists, amis
    print("Creating the mariadb databases")
    spotifree = BDD(spotify_data=spotify_data)
    spotifree.creation_bdd()
    
    

###################  MAIN  #########################
# décommenter spotify_donnees() pour relancer l'extraction de données spotify (après avoir modifier les artistes à chercher par exemples)
# spotify_donnees()

# si le fichier BDD/spotify_bdd.json existe déjà, on peut juste lancer la fonction bdd pour créer la bdd sql
bdd()
