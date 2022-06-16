FROM archlinux
WORKDIR /usr/src/app

# Téléchargement nécessaire pour lancer et faire fonctionner spotifree 
RUN pacman -Sy --noconfirm
RUN pacman -S python3 --noconfirm
RUN pacman -S python-flask --noconfirm
RUN pacman -S python-flask-login --noconfirm
RUN pacman -S python-flask-sqlalchemy --noconfirm
RUN pacman -S python-pip --noconfirm 
RUN pip install flask-mysql

# Copie du fichier hosts pour avoir un joli nom de domaine 
COPY hosts /etc/hosts

# Copie de toutes les scripts flask en python necessaire pour faire fonctionner spotifree 
COPY main.py /home/main.py
COPY website/ /home/website/
COPY __pycache__/ /home/__pycache__/
COPY __init__.py /home/__init__.py

# Lancement de spotifree 
ENTRYPOINT FLASK_APP=/home/main.py flask run --host=0.0.0.0