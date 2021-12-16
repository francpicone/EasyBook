import mysql.connector
from flask import current_app, g
from flask.cli import with_appcontext

def initialize_db():

        db = mysql.connector.connect(host="localhost",
                                    port="3306",  # your host, usually localhost
                                    user="root",  # your username
                                    passwd="pass123",  # your password
                                    db="EasyBook")  # name of the data base

        cur = db.cursor()

        return cur




