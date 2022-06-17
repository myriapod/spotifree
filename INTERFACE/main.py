# Après avoir lancé le flask en local, démarré le script main.py avec python3
# Permet la connexion sur la page html spotifree
from INTERFACE.website import create_app

app = create_app()

app.run(host="127.0.0.1", port=5000, debug = True)
