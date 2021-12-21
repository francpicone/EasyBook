import mysql.connector
import db
from flask import (
    Blueprint, g, redirect, render_template, url_for
)

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    if g.user is not None:  # Se g.user non è nullo, quindi ho un utente loggato, reindirizzo il browser alla homapage
        print(g.user)

        dbconn = mysql.connector.connect(**db.get_config())
        cursor = dbconn.cursor()
        get_books = 'SELECT * FROM LIBRO'
        data = ()
        cursor.execute(get_books)
        libri = cursor.fetchall()

        return render_template('homepage.html', books=libri)
    else:  # Diversamente, se g.user è None, quindi non ho un utente loggato, reindirizzo il browser alla pagina di login
        return redirect(url_for('auth.login'))


