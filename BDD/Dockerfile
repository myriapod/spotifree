FROM mariadb:latest

RUN apt-get update \
    && apt-get -yy install libmariadb-dev \
    && apt-get -y install python3 \
    && apt-get -y install python3-pip

RUN mkdir -p /opt/spotifree/BDD

COPY requirements.txt /opt/spotifree/BDD/requirements.txt

WORKDIR /opt/spotifree/BDD

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . ./
RUN ls

CMD ["/main_bdd.py"]
ENTRYPOINT ["python3"]