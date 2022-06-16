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

- pour rajouter des artistes dans la BDD spotify: modifier la liste <code>liste_famous_singers</code> de <code>BDD/main_bdd.py</code>

<h2>Encore en phase de test</h2>
<h3>docker file bdd</h3>
lancer:

```
# docker build -t spotifreebdd /PATH/TO/spotifree/BDD
# docker run -d spotifreebdd /PATH/TO/spotifree/BDD
```

Dans le <code>main_bdd.py</code> on peut commenter <code>spotify_donnees()</code> pour ne pas relancer le chargement de la BDD à partir de spotify. (Les données sont enregistrées dans un fichier .json intermédiaire).
