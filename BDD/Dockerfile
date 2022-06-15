FROM archlinux

RUN pacman -Syu --noconfirm --disable-download-timeout
# besoin de --disable-download-timeout sinon un paquet bloque
# besoin de gcc pour python mariadb
RUN pacman -S gcc --noconfirm


# set up mariadb

RUN pacman -S mariadb --noconfirm

EXPOSE 3306

LABEL version="1.0"
LABEL description="MariaDB Server"

# RUN mysqld

RUN mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
RUN systemctl start mariadb.service

RUN pacman -S python --noconfirm
RUN pacman -S python-pip --noconfirm

RUN mkdir -p /opt/spotifree/BDD

COPY requirements.txt /opt/spotifree/BDD/requirements.txt

WORKDIR /opt/spotifree/BDD

RUN pip install -r requirements.txt
COPY . ./

RUN /bin/python main_bdd.py