from BDD.classes import BDD, Spotify_Artist, Spotify_Albums, Spotify_Tracks
import json
import os


LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'



###################  DONNEES SPOTIFY  #######################

def spotify_donnees():
    # https://www.songkick.com/leaderboards/popular_artists 
    list_famous_singers = ['rihannah', 'coldplay', 'eminem', 'seventeen', 'monsta x', 'loona']


    # alternative: passer par un main différent pour créer la base de donnée spotify, mettre la spotify_data dans un .json
    index = [0]
    spotify_data = []
    print("Extracting data from spotify\n")
    for artist in list_famous_singers:
        print(LINE_UP, end=LINE_CLEAR)
        print(f" > Working on {artist}...")
        
        artist = Spotify_Artist(artist)
        
        album = Spotify_Albums(artist.artist_ID)
        
        for i in range(len(album.album_ids)):
            tracks = Spotify_Tracks(album.album_ids[i], album.album_names[i], spotify_data, index)
            
    # on rajoute un file json pour garder en mémoire les données sans devoir extraire à nouveau d'internet (ça prend du temps)
    with open('BDD/spotify_bdd.json', 'w') as output_file:
        json.dump(spotify_data, output_file)

    print(LINE_UP, end=LINE_CLEAR)
    print("Spotify data collected.")



###################  BDD  #########################

def bdd():
    with open('BDD/spotify_bdd.json', 'r') as input_file:
        spotify_data = json.load(input_file)
    # print(spotify_data)

    # création de la bdd spotifree et des tables 
    print("Creating the mariadb databases")
    spotifree = BDD(spotify_data=spotify_data)
    spotifree.creation_bdd() # creation de la bdd ok
    
    

###################  MAIN  #########################
# database ok, tout est dans le BDD/spotify_bdd.json
# spotify_donnees()

# si le fichier BDD/spotify_bdd.json existe déjà, on peut juste lancer la fonction bdd pour créer la bdd sql
bdd()