FROM archlinux

# Téléchargement nécessaire pour lancer et faire fonctionner spotifree 
RUN pacman -Sy --noconfirm
RUN pacman -S python --noconfirm
RUN pacman -S python-pip --noconfirm
RUN pip install flask

# Copie de toutes les scripts flask en python necessaire pour faire fonctionner spotifree 
COPY spotifree.py /home/spotifree.py
# rajouter la copie de toutes les pages 

# Lancement de spotifree 
ENTRYPOINT SPOTIFREE=/home/spotifree.py flask run --host=127.0.0.1
