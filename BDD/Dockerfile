# dockerfile pour faire tourner la base de données
# pas bien testée et ne marche pas très bien
FROM mariadb:latest

# installation de tous les paquets nécessaires
RUN apt-get update \
    && apt-get -yy install libmariadb-dev \
    && apt-get -y install python3 \
    && apt-get -y install python3-pip

# création du dossier spotifree/BDD
RUN mkdir -p /opt/spotifree/BDD

COPY requirements.txt /opt/spotifree/BDD/requirements.txt

WORKDIR /opt/spotifree/BDD

# installation des requirements pour python
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . ./

# lancement du programme
CMD ["main_bdd.py"]
ENTRYPOINT ["python3"]
