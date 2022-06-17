# spotifree
équivalent à spotify


groupe 3  - Jenny  - Yasmine - Maureen - Solene - Sidney

<a href="https://whiteboard.office.com/me/whiteboards/p/c3BvOmh0dHBzOi8vbGFib20yaWZvcm1hdGlvbi1teS5zaGFyZXBvaW50LmNvbS9wZXJzb25hbC9zaWRuZXlfc2FsZXNfbGFib20yaWZvcm1hdGlvbl9mcg%3D%3D/b!UmOdbVgs7E66p-9vWgpBmBfbhuBxV-JGoc9vj0Kp2jfj8XDvg7ZRS5ufKngpVHMl/015BLRSVBQFIEXHSRL65C2MVH2ROJP6DZC">whiteboard</a>

<h2>Lancer Spotifree</h2>

```
pip install -r requirements.txt
python spotifree.py
```

aller sur <a href='http://127.0.0.1:5000/'>http://127.0.0.1:5000</a>

- il est possible qu'il soit nécessaire de changer les identifiants root mariadb dans <code>BDD/classes.py</code> et <code>SERVEUR/classes_srv.py</code>

- pour lancer spotifree en ligne de commande:

```
python SERVEUR/main.py
```

- pour rajouter des artistes dans la BDD spotify: modifier la liste <code>list_artists</code> de <code>BDD/main_bdd.py</code>


<h2>API Spotify et téléchargement des musiques</h2>

Le <a href="https://developer.spotify.com/">Spotify for Developers</a> permet d'avoir accés à des credentials spotify qui sont nécessaire pour utiliser <a href="https://spotipy.readthedocs.io/en/2.19.0/">spotipy</a> et extraire des données spotify. Le processus d'extraction des données est développé dans les commentaires du fichier <code>BDD/classes.py (partie SPOTIFY)</code>.

Pour télécharger les musiques (sur Youtube) à partir d'un lien spotify: <a href="https://github.com/spotDL/spotify-downloader">spotify-downloader</a>


<h2>Utilisation de Flask</h2>

Flask est un framework open-source de développement web en Python, classé comme "micro framework" car très léger. Malgré l'absence des fonctionnalité de bases nécessaires à l'exercice (système d'authentification, abstraction de base de données ou validation de formulaires), il permet cependant l'installation d'extensions et intègre un moteur de gestion de templates pour du rendu HTML, qui ont rendu le développement de cette application possible.

La très belle architecture du site, conçue par le M2I-Formation-Groupe3™, dont le génie collectif ne peut être égalé que par leur folie individuelle, provient de multitudes d'exemples glanés sur internet après des fouilles intensives sur des sites peu connus, voir obscurs, tels que W3school, Github, Stack Overflow, Youtube, et de nombreuses autres provinces du web, dont l'énumération serait inutile et fastidueuse...

(Même si en vrai un très grosse partie fût peu scrupuleusement repompée sur le github suivant : https://github.com/techwithtim/Flask-Web-App-Tutorial)



<h2>Encore en phase de test</h2>
<h3>docker file bdd</h3>
lancer:

```
# docker build -t spotifreebdd /PATH/TO/spotifree/BDD
# docker run -d spotifreebdd /PATH/TO/spotifree/BDD
```

Dans le <code>main_bdd.py</code> on peut commenter <code>spotify_donnees()</code> pour ne pas relancer le chargement de la BDD à partir de spotify. (Les données sont enregistrées dans un fichier .json intermédiaire).

<h3>docker file flask</h3>

```
sudo docker build -t flask-spotifree -f ./flask.dockerfile .
sudo docker run -p 5000:5000 flask-spotifree
```

aller sur <a href="www.spotifree.fr:5000">www.spotifree.fr:5000</a>

pour accéder à www.spotifree.fr directement, il faut modifier dans le <code>INTERFACE/main.py</code> le port 80 et lancer

```
sudo docker run -p 80:5000 flask-spotifree
```
