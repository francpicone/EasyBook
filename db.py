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
        dbconn.commit()


