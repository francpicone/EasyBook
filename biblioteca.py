from werkzeug.security import generate_password_hash, check_password_hash

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
    q_get_aut = ('select AUTORE.nome as nome, AUTORE.cognome as cognome from AUTORE join LIBRO on LIBRO.autore_lib=AUTORE.id_aut where ISBN=%s')
    q_get_gen = ('select descrizione_genere as genere_libro from GENERE join LIBRO on LIBRO.genere_lib=GENERE.id_genere WHERE ISBN=%s')
    q_get_edit = ('select EDITORE.nome as editore_libro from EDITORE join LIBRO on LIBRO.editore_lib=EDITORE.id_editore WHERE ISBN=%s')
    q_get_disp = ('select BIBLIOTECA.Nome as Biblioteca, count(num_copia) as numero_copie_libro from COPIA_LIBRO join BIBLIOTECA on BIBLIOTECA.id_biblioteca=COPIA_LIBRO.id_bibl_copia WHERE ISBN=%s GROUP BY BIBLIOTECA.Nome')

    cursor.execute(q_get_book, (bookid,))
    libro = cursor.fetchone()

    cursor.execute(q_get_aut, (bookid,))
    aut = cursor.fetchall()

    cursor.execute(q_get_gen, (bookid,))
    gen = cursor.fetchall()

    cursor.execute(q_get_edit, (bookid,))
    edit = cursor.fetchall()

    cursor.execute(q_get_disp, (bookid,))
    disp = cursor.fetchall()

    cursor.close()
    dbconn.close()

    return render_template('biblioteca/libro.html', book=libro, autori=aut, generi=gen, editori=edit, disponibili=disp)

@bp.route('/biblioteca/<bibid>')
@auth.login_required
def get_biblioteca(bibid):

    dbconn = mysql.connector.connect(**db.get_config())
    cursor = dbconn.cursor()

    q_get_libro = 'SELECT * FROM BIBLIOTECA WHERE Id_biblioteca = %s'
    cursor.execute(q_get_libro, (bibid,))
    bib = cursor.fetchone()

    return render_template('biblioteca/biblioteca.html', biblioteca=bib)

