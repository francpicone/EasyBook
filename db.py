import mysql.connector
from flask import current_app, g
from flask.cli import with_appcontext


def get_config():
    config = {
        'user': 'root',
        'password': 'pass123',
        'host': 'localhost',
        'port': '6033',
        'database': 'easybook'
    }
    return config  # restituisce i parametri di connessione al database


