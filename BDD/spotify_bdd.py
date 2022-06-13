# creation de la bdd pour un utilisateur en lui donnant des identifiants mariadb

# https://github.com/plamere/spotipy 
# doc: https://spotipy.readthedocs.io/en/2.19.0/ 

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

# credentials du projet spotifree
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="2bc3eddc577f4e4496d29334479f1780",
                                                           client_secret="174417f6ba92480789f1d88734a9c3e4"))


class Spotify_Artist():
    def __init__(self, artist):
        self.results = sp.search(q=artist, limit=20, type="artist") # on cherche les 20 premiers résultats qui correspondent au nom de l'artiste
        items = self.results["artists"]["items"]
        if len(items) != 0:
            d = items[0]

        self.artist_ID = d["id"] # on récupère l'id spotify de l'artiste


class Spotify_Albums():
    def __init__(self, artist_id):
        self.results = sp.artist_albums(artist_id=artist_id, limit=50) # à partir de l'id de l'artiste on peut afficher ses 50 premiers albums
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
        self.results = sp.album_tracks(album_id=album_id, limit=20) # à partir de l'id de l'album, on peut afficher les 20 premières chansons dedans
        
        for track in self.results['items']:
            index.append(index[-1]+1) # un peu bizzare mais ça permet de donner un track_id unique
            # on ajoute directement à la liste de dictionnaire des chansons chaque chanson de l'album
            data.append({'track_id' : index[-1],
                          'artist_name' : track['artists'][0]['name'],
                          'album_name' : album_name,
                          'track_name' :  track['name'],
                          'track_number' : track['track_number']
                        })



###main###

# https://www.songkick.com/leaderboards/popular_artists 
list_famous_singers = ['Rihanna', 'Drake', 'Coldplay', 'Eminem', 'Maroon 5', 'Ed Sheeran', 'Bruno Mars' ,'Kanye West', 'Adele' ,'The Weeknd' ,'U2',
    'Beyoncé', 'Justin Bieber', 'Taylor Swift', 'Katy Perry', 'Kendrick Lamar', 'Red Hot Chili Peppers' ,'Lil Wayne', 'Nicki Minaj', 'Calvin Harris' ,'Imagine Dragons'
    'Lady Gaga', 'Ariana Grande', 'Queen', 'Usher', 'Radiohead', 'Kings of Leon', 'Arctic Monkeys', 'Ellie Goulding', 'Pitbull', 'Post Malone', 'Green Day']


with open('BDD/spotify_bdd.json', 'w') as f:
    
    index = [0,1]
    data = []
    for artist in list_famous_singers:
        
        artist = Spotify_Artist('artist')
        
        album = Spotify_Albums(artist.artist_ID)
        
        for i in range(len(album.album_ids)):
            tracks = Spotify_Tracks(album.album_ids[i], album.album_names[i], data, index)
            
    
    # on met la liste de dictionnaire dans un fichier json
    json.dump(data, f)
    
            
