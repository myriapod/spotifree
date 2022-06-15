FROM mariadb:latest

RUN apt-get update \
    && apt-get -yy install libmariadb-dev

RUN mkdir -p /opt/spotifree/BDD

COPY requirements.txt /opt/spotifree/BDD/requirements.txt

WORKDIR /opt/spotifree/BDD

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . ./
RUN ls

# marche pas, y a pas mariadb de lancé
CMD ["python", "main_bdd.py"]