import mysql.connector
from flask import current_app, g
from flask.cli import with_appcontext


def get_config():
    config = {
        'user': 'db_user',
        'password': 'db_user_pass',
        'host': 'db',
        'port': '3306',
        'database': 'easybook'
    }
    return config  # restituisce i parametri di connessione al database


def initdb():       #Inizializza un database di prova

    dbconn = mysql.connector.connect(**get_config())

    with open('easybook.sql', 'r') as f:
        with dbconn.cursor() as cursor:
            cursor.execute(f.read(), multi=True)

    cursor.close()
    dbconn.close()

def populatedb():

    dbconn = mysql.connector.connect(**get_config())
    mycursor = dbconn.cursor()

    q_insert_editore = 'INSERT INTO EDITORE (id_editore, nome) VALUES (0,%s)'
    q_insert_genere = 'INSERT INTO GENERE (id_genere, descrizione_genere) VALUES (0,%s)'
    q_insert_biblioteca = 'INSERT INTO BIBLIOTECA (Id_biblioteca,Nome,Num_telefono,Indirizzo,Cord_X,Cord_Y,Posti_aula_studio) values (%s,%s,%s,%s,%s,%s,%s)'
    q_insert_utente_prova = 'INSERT INTO UTENTE (nome_ut, cognome_ut, email, CF, sesso, data_nascita, PW, QR, citta_ut, token_ut, admin) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    editori = ['McGraw-Hill', 'Zanichelli', 'Addison-Wesley Professional', 'Mondadori', 'Bompiani',
               'Sperling Paperback', 'Feltrinelli']

    generi = ['Informatica', 'Romanzo', 'Fantasy', 'Horror', 'Tragedia', 'Poema', 'Saggio']

    for editore in editori:
        mycursor.execute(q_insert_editore, (editore, ))
        dbconn.commit()

    for genere in generi:
        mycursor.execute(q_insert_genere, (genere, ))
        dbconn.commit()

    mycursor.execute(q_insert_biblioteca, (0, 'Biblioteca Comunale di Pomigliano', '3388354219', 'Corso Vittorio Emanuele', 40.9087, 14.3875, 60, ))
    dbconn.commit()

    mycursor.execute(q_insert_utente_prova, ('Biblioteca Comunale', 'di Pomigliano', 'bibpom@bib.it', '438589358973', None, '2021-12-16', 'pbkdf2:sha256:260000$6OYb5LvgfNxlLgzn$ca4ee2a25643961221a41c42f7d77af6d5389b3e3d8028ec6c66600082a833c2', None, 'Pomigliano', 'liykltetegebpxfykbvrsdnpduvdnbdlhwwfxowullbrapaqgdviitvsnrhmvpob', 1, ))
    dbconn.commit()

    mycursor.close()
    dbconn.close()

