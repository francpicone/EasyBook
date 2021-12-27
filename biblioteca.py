import auth, db, Homepage
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import mysql.connector

bp = Blueprint('biblioteca', __name__)


@bp.route('/libro/<bookid>')
@auth.login_required
def get_libro(bookid):
    dbconn = mysql.connector.connect(**db.get_config())
    cursor = dbconn.cursor()
    q_get_book = ('SELECT * FROM LIBRO WHERE ISBN = %s')
    q_get_aut = ('select AUTORE.nome as nome, AUTORE.cognome as cognome from AUTORE join LIBRO on LIBRO.autore_lib=AUTORE.id_aut')

    cursor.execute(q_get_book, (bookid,))
    libro = cursor.fetchone()

    cursor.execute(q_get_aut)
    aut = cursor.fetchall()

    cursor.close()
    dbconn.close()

    return render_template('biblioteca/libro.html', book=libro, autori=aut)
