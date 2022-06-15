FROM archlinux

# Téléchargement nécessaire pour lancer et faire fonctionner spotifree 
RUN pacman -Sy --noconfirm
RUN pacman -S python3 --noconfirm
RUN pacman -S python-flask --noconfirm
RUN pacman -S python-flask-login --noconfirm
# RUN pip install flask

COPY hosts /etc/hosts

# Copie de toutes les scripts flask en python necessaire pour faire fonctionner spotifree 
COPY main.py /home/main.py
COPY templates/ /home/templates/


# Lancement de spotifree 
ENTRYPOINT FLASK_APP=/home/main.py flask run --host=0.0.0.0 