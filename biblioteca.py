from datetime import date, timedelta

from werkzeug.security import generate_password_hash, check_password_hash

import auth, db, Homepage
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
import mysql.connector

bp = Blueprint('biblioteca', __name__)


@bp.route('/libro/<bookid>')
@auth.login_required
def get_libro(bookid):
    dbconn = mysql.connector.connect(**db.get_config())
    cursor = dbconn.cursor()
    q_get_book = ('SELECT * FROM LIBRO WHERE ISBN = %s')
    q_get_aut = (
        'select AUTORE.nome as nome, AUTORE.cognome as cognome from AUTORE join LIBRO on LIBRO.autore_lib=AUTORE.id_aut where ISBN=%s')
    q_get_gen = (
        'select descrizione_genere as genere_libro from GENERE join LIBRO on LIBRO.genere_lib=GENERE.id_genere WHERE ISBN=%s')
    q_get_edit = (
        'select EDITORE.nome as editore_libro from EDITORE join LIBRO on LIBRO.editore_lib=EDITORE.id_editore WHERE ISBN=%s')
    q_get_disp = (
        'select BIBLIOTECA.Id_biblioteca as ID, BIBLIOTECA.Nome as Biblioteca, count(num_copia) as numero_copie_libro from COPIA_LIBRO join BIBLIOTECA on BIBLIOTECA.id_biblioteca=COPIA_LIBRO.id_bibl_copia WHERE ISBN=%s AND Disponibile=1 GROUP BY ID')

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

    c_posti_prenotati = None
    c_posti_totali = None
    posti_totali = None
    posti_disponibili = None
    bib = None

    error = None
    try:
        q_get_biblioteca = 'SELECT * FROM BIBLIOTECA WHERE Id_biblioteca = %s'
        cursor.execute(q_get_biblioteca, (bibid,))
        bib = cursor.fetchone()

       # q_get_posti_totali = 'SELECT COUNT(Id_posto) as NumeroPostiDisponibili, BIBLIOTECA.Nome as Biblioteca, Disponibile FROM POSTO JOIN BIBLIOTECA ON Id_biblioteca_posto = BIBLIOTECA.Id_biblioteca WHERE BIBLIOTECA.Id_biblioteca = %s GROUP BY Id_posto'
        q_get_posti_totali = 'SELECT Posti_aula_studio FROM BIBLIOTECA WHERE Id_biblioteca = %s'
        cursor.execute(q_get_posti_totali, (bibid,))
        c_posti_totali = cursor.fetchone()

        q_get_posti_prenotati = 'SELECT COUNT(Id_prenotazione) as NumeroPrenotazioni, BIBLIOTECA.Nome AS NomeBiblioteca FROM PRENOTAZIONI_POSTO JOIN BIBLIOTECA ON Id_biblioteca_prenotazione = BIBLIOTECA.Id_biblioteca WHERE BIBLIOTECA.Id_Biblioteca = %s AND Data_prenotazione = %s GROUP BY PRENOTAZIONI_POSTO.Id_biblioteca_prenotazione'
        cursor.execute(q_get_posti_prenotati, (bibid, date.today()))
        c_posti_prenotati = cursor.fetchone()

    except:
        error = 'E'' stato riscontrato un errore'

    if error is None:

        if c_posti_totali is None and c_posti_prenotati is None:
            posti_disponibili = 0
            posti_totali = 0

        elif c_posti_prenotati is None:
            posti_totali = c_posti_totali[0]
            posti_disponibili = posti_totali
        else:
            posti_disponibili = c_posti_totali[0] - c_posti_prenotati[0]

    cursor.close()
    dbconn.close()

    return render_template('biblioteca/biblioteca.html', biblioteca=bib, posti_disponibili=posti_disponibili,
                           posti_totali=posti_totali, data_odierna=date.today())


@bp.route('/checkpostidisponibili', methods=('GET', 'POST'))
@auth.login_required
def check_posti_disponibili():
    if request.method == 'GET':
        data = request.args['data']
        bibid = request.args['bibid']

        error = None
        posti_totali = None
        posti_prenotati = None

        try:

            dbconn = mysql.connector.connect(**db.get_config())
            cursor = dbconn.cursor()

           # q_get_posti_totali = 'SELECT COUNT(Id_posto) as NumeroPostiDisponibili, BIBLIOTECA.Nome as Biblioteca, Disponibile FROM POSTO JOIN BIBLIOTECA ON Id_biblioteca_posto = BIBLIOTECA.Id_biblioteca WHERE BIBLIOTECA.Id_biblioteca = %s GROUP BY Id_posto'
            q_get_posti_totali = 'SELECT Posti_aula_studio FROM BIBLIOTECA WHERE Id_biblioteca = %s'
            cursor.execute(q_get_posti_totali, (bibid,))
            c_posti_totali = cursor.fetchone()

            print(c_posti_totali[0])

            q_get_posti_prenotati = 'SELECT COUNT(Id_prenotazione) as NumeroPrenotazioni, BIBLIOTECA.Nome AS NomeBiblioteca FROM PRENOTAZIONI_POSTO JOIN BIBLIOTECA ON Id_biblioteca_prenotazione = BIBLIOTECA.Id_biblioteca WHERE BIBLIOTECA.Id_Biblioteca = %s AND Data_prenotazione = %s GROUP BY PRENOTAZIONI_POSTO.Id_biblioteca_prenotazione'
            cursor.execute(q_get_posti_prenotati, (bibid, data))
            c_posti_prenotati = cursor.fetchone()

        except:
            error = 'E'' stato riscontrato un errore'
            return jsonify(status='error')

        if error is None:

            if c_posti_totali is None and c_posti_prenotati is None:
                posti_disponibili = 0
                posti_totali = 0

            elif c_posti_prenotati is None:
                posti_totali = c_posti_totali[0]
                posti_disponibili = posti_totali
            else:
                posti_disponibili = c_posti_totali[0] - c_posti_prenotati[0]

            return jsonify(status='ok',
                           posti_totali=posti_totali,
                           posti_disponibili=posti_disponibili)


@bp.route('/libreria')
@auth.login_required
def get_libreria():
    dbconn = mysql.connector.connect(**db.get_config())
    cursor = dbconn.cursor()

    q_get_libreria = (
        'SELECT * FROM LIBRO join COPIA_LIBRO ON COPIA_LIBRO.isbn = LIBRO.ISBN join BIBLIOTECA ON BIBLIOTECA.Id_biblioteca = COPIA_LIBRO.id_bibl_copia join PRENDE_IN_PRESTITO on PRENDE_IN_PRESTITO.num_copia_prestito=COPIA_LIBRO.num_copia join UTENTE on PRENDE_IN_PRESTITO.codice_fiscale=UTENTE.CF WHERE CF = %s')
    cursor.execute(q_get_libreria, (g.user[3],))
    libreria = cursor.fetchall()

    cursor.close()
    dbconn.close()

    return render_template('biblioteca/libreria_utente.html', books=libreria)


@bp.route('/prenota', methods=('GET', 'POST'))
@auth.login_required
def prenota_libro():
    if request.method == 'POST':
        biblioteca = request.form['bib']
        isbn = request.form['isbn']

        error = None

        dbconn = mysql.connector.connect(**db.get_config())

        cursor = dbconn.cursor()

        # Controllo che l'utente non abbia un'ulteriore copia del libro prenotata
        q_check_libro = (
            'SELECT num_copia AS numero_copia, isbn as isbn, codice_fiscale as CF FROM COPIA_LIBRO JOIN PRENDE_IN_PRESTITO ON num_copia=num_copia_prestito WHERE isbn=%s and codice_fiscale=%s')
        cursor.execute(q_check_libro, (isbn, g.user[3]))

        if cursor.fetchone() is not None:
            return jsonify(status='alreadybooked',
                           msg='Libro già in libreria!',
                           )
        # Fine del controllo

        # Seleziono un libro fisico disponibile e prelevo il numero identificativo della copia
        q_get_libro = ('SELECT * FROM COPIA_LIBRO WHERE isbn=%s and id_bibl_copia=%s and Disponibile=1 LIMIT 1')
        cursor.execute(q_get_libro, (isbn, biblioteca))

        num_copia = cursor.fetchone()
        print(num_copia)

        try:
            # Rendo non disponibile la copia
            q_prenota_libro = ('UPDATE `COPIA_LIBRO` SET `Disponibile`= 0 WHERE num_copia = %s')
            cursor.execute(q_prenota_libro, (num_copia[0],))
            dbconn.commit()

            # Inserisco la copia prenotata nella liberia dell'utente
            q_set_libro_utente = (
                'INSERT INTO `PRENDE_IN_PRESTITO`(`Id_prestito`,`codice_fiscale`, `num_copia_prestito`, `data_prestito`, `data_di_restituzione`, `restituito`) VALUES (0,%s,%s,%s,%s,%s)')
            cursor.execute(q_set_libro_utente,
                           (g.user[3], num_copia[0], date.today(), date.today() + timedelta(days=15), 0,))
            dbconn.commit()

        except:
            error = 'E'' stato riscontrato un errore'
            print(error)

        if error is None:
            cursor.close()
            dbconn.close()

            return jsonify(status='ok',
                           msg='Libro prenotato con successo !',
                           bib=biblioteca,
                           isbn=isbn,
                           num_copia=num_copia[0]
                           )


@bp.route('/annullaprenotazione', methods=('GET', 'POST'))
@auth.login_required
def annulla_prenotazione():
    if request.method == 'POST':
        IDPrestito = request.form['idprestito']

        error = None

        q_get_libreria = (
            'SELECT * FROM LIBRO join COPIA_LIBRO ON COPIA_LIBRO.isbn = LIBRO.ISBN join BIBLIOTECA ON BIBLIOTECA.Id_biblioteca = COPIA_LIBRO.id_bibl_copia join PRENDE_IN_PRESTITO on PRENDE_IN_PRESTITO.num_copia_prestito=COPIA_LIBRO.num_copia join UTENTE on PRENDE_IN_PRESTITO.codice_fiscale=UTENTE.CF WHERE CF = %s AND Id_prestito = %s')

        try:
            dbconn = mysql.connector.connect(**db.get_config())
            cursor = dbconn.cursor()
            cursor.execute(q_get_libreria, (g.user[3], IDPrestito))
            prestito = cursor.fetchone()
            print(prestito)

            # Rendo di nuovo disponibile il libro
            q_set_libro_disponibile = ('UPDATE `COPIA_LIBRO` SET `Disponibile`= 1 WHERE num_copia = %s')
            cursor.execute(q_set_libro_disponibile, (prestito[10],))
            dbconn.commit()

            # Elimino il libro dai prestiti
            q_delete_from_libreria = ('DELETE FROM `PRENDE_IN_PRESTITO` WHERE Id_prestito=%s')
            cursor.execute(q_delete_from_libreria, (IDPrestito,))
            dbconn.commit()
            print('commit2')

            cursor.close()
            dbconn.close()

        except:
            error = "E'' stato riscontrato un errore"
            print(error)

        if error is None:
            return jsonify(status='ok',
                           msg='Prenotazione annullata con successo.',
                           IDPrestito=IDPrestito)


@bp.route('/search', methods=('GET', 'POST'))
@auth.login_required
def search():
    if request.method == 'GET':
        # data = request.form['search']
        data = '%' + request.args['search'] + '%'
        dbconn = mysql.connector.connect(**db.get_config())

        print(data)

        q_search_libri = (
            'SELECT ISBN, titolo, AUTORE.nome AS Nome_autore, AUTORE.cognome as cognome_autore, GENERE.descrizione_genere as genere, valutazione, edizione, EDITORE.nome as Nome_editore, copertina FROM LIBRO JOIN AUTORE ON LIBRO.autore_lib = AUTORE.id_aut JOIN GENERE ON LIBRO.genere_lib = GENERE.id_genere JOIN EDITORE ON LIBRO.editore_lib = EDITORE.id_editore WHERE titolo LIKE %s OR ISBN=%s OR AUTORE.nome LIKE %s OR AUTORE.cognome LIKE %s OR GENERE.descrizione_genere LIKE %s OR EDITORE.nome LIKE %s')

        q_search_biblioteche = ('SELECT * FROM `BIBLIOTECA` WHERE Nome LIKE %s OR Indirizzo LIKE %s')

        try:
            cursor = dbconn.cursor()
            cursor.execute(q_search_libri, (data, data, data, data, data, data))
            results_libri = cursor.fetchall()

            cursor.execute(q_search_biblioteche, (data, data))
            results_biblioteche = cursor.fetchall()

            return render_template('biblioteca/search_results.html', results_libri=results_libri, results_biblioteche=results_biblioteche)

        except:
            error = 'E'' stato riscontrato un errore'
            print(error)

@bp.route('/prenotaaula', methods=('GET', 'POST'))
@auth.login_required
def prenota_aula():
        if request.method == 'POST':
            content = request.get_json()
            data = content['data']
            bibid = content['bibid']

            dbconn = mysql.connector.connect(**db.get_config())
            cursor = dbconn.cursor()

            error = None

            q_controllo_prenotazione = ('SELECT UTENTE.CF, Id_prenotazione, BIBLIOTECA.Id_biblioteca FROM `PRENOTAZIONI_POSTO` JOIN UTENTE ON Utente = UTENTE.CF JOIN BIBLIOTECA ON Id_biblioteca_prenotazione = BIBLIOTECA.Id_biblioteca WHERE CF = %s AND Data_prenotazione = %s AND BIBLIOTECA.Id_biblioteca = %s')
            cursor.execute(q_controllo_prenotazione, (g.user[3], data, bibid))
            check = cursor.fetchone()

            if check is not None:
                error = 'Prenotazione già effettuata in questa data per questa biblioteca.'
                return jsonify(status="error",
                               msg=error)
            else:

                try:
                    q_prenota_posto = ('INSERT INTO `PRENOTAZIONI_POSTO`(`Id_prenotazione`, `Id_biblioteca_prenotazione`, `Utente`, `Data_prenotazione`) VALUES (%s,%s,%s,%s)')
                    cursor.execute(q_prenota_posto, (0, bibid, g.user[3], data))
                    dbconn.commit()
                    cursor.close()
                    dbconn.close()

                except:
                    error = 'E'' stato riscontrato un errore'
                    print(error)

            if error is None:
                return jsonify(status="ok")

@bp.route('/prenotazioni', methods=('GET', 'POST'))
@auth.login_required
def get_prenotazioni():

    dbconn = mysql.connector.connect(**db.get_config())
    cursor = dbconn.cursor()

    q_get_prenotazioni = 'SELECT Id_prenotazione, UTENTE.CF, Data_prenotazione, BIBLIOTECA.Nome, BIBLIOTECA.Id_biblioteca FROM PRENOTAZIONI_POSTO JOIN UTENTE ON Utente = UTENTE.CF JOIN BIBLIOTECA ON Id_biblioteca_prenotazione = BIBLIOTECA.Id_biblioteca WHERE UTENTE.CF = %s'

    cursor.execute(q_get_prenotazioni, (g.user[3], ))
    prenotazioni = cursor.fetchall()

    return render_template('biblioteca/prenotazioni_utente.html', prenotazioni=prenotazioni)
