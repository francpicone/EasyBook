from datetime import date

import mysql.connector

import auth
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
        get_books = 'SELECT * FROM LIBRO JOIN AUTORE ON autore_lib = AUTORE.id_aut JOIN GENERE ON genere_lib = GENERE.id_genere'
        cursor.execute(get_books)
        libri = cursor.fetchall()

        return render_template('homepage.html', books=libri)
    else:  # Diversamente, se g.user è None, quindi non ho un utente loggato, reindirizzo il browser alla pagina di login
        return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@auth.login_required
def dashboard():

    if g.user[10] is None:
        return redirect(url_for('home.index'))

    else:
        dbconn = mysql.connector.connect(**db.get_config())
        cursor = dbconn.cursor()

        q_get_prestiti_totali = 'SELECT COUNT(*) FROM PRENDE_IN_PRESTITO JOIN COPIA_LIBRO ON num_copia_prestito = COPIA_LIBRO.num_copia WHERE COPIA_LIBRO.id_bibl_copia = %s'
        q_get_prenotazioni_totali = 'SELECT COUNT(*) FROM PRENOTAZIONI_POSTO WHERE Id_biblioteca_prenotazione = %s'
        q_get_prestiti_attivi = 'SELECT COUNT(*) FROM PRENDE_IN_PRESTITO JOIN COPIA_LIBRO ON num_copia_prestito = COPIA_LIBRO.num_copia WHERE COPIA_LIBRO.id_bibl_copia = %s AND restituito<=1'
        q_get_prenotazioni_attive = 'SELECT COUNT(*) FROM PRENOTAZIONI_POSTO WHERE Id_biblioteca_prenotazione = %s AND Data_prenotazione >= %s'

        cursor.execute(q_get_prestiti_totali, (g.user[10], ))
        prestiti_totali = cursor.fetchone()

        cursor.execute(q_get_prenotazioni_totali, (g.user[10], ))
        prenotazioni_totali = cursor.fetchone()

        cursor.execute(q_get_prestiti_attivi, (g.user[10], ))
        prestiti_attivi = cursor.fetchone()

        cursor.execute(q_get_prenotazioni_attive, (g.user[10], date.today()))
        prenotazioni_attive = cursor.fetchone()

        q_get_ultimi_prestiti = 'SELECT Id_prestito, codice_fiscale, data_prestito, data_di_restituzione, restituito, LIBRO.ISBN, LIBRO.titolo, LIBRO.copertina, UTENTE.nome_ut, UTENTE.cognome_ut FROM PRENDE_IN_PRESTITO JOIN COPIA_LIBRO ON num_copia_prestito = COPIA_LIBRO.num_copia JOIN LIBRO ON COPIA_LIBRO.isbn = LIBRO.ISBN JOIN UTENTE ON codice_fiscale = UTENTE.CF WHERE id_bibl_copia = %s LIMIT 15'
        cursor.execute(q_get_ultimi_prestiti, (g.user[10], ))
        ultimi_prestiti = cursor.fetchall()

        q_get_ultime_prenotazioni = 'SELECT Id_prenotazione, Data_prenotazione, UTENTE.nome_ut, UTENTE.cognome_ut, UTENTE.email FROM `PRENOTAZIONI_POSTO` JOIN UTENTE ON Utente = UTENTE.CF WHERE Id_biblioteca_prenotazione = %s'
        cursor.execute(q_get_ultime_prenotazioni, (g.user[10],))
        ultime_prenotazioni = cursor.fetchall()

    return render_template('admindashboard.html', prestiti_totali=prestiti_totali[0], prenotazioni_totali=prenotazioni_totali[0], prestiti_attivi=prestiti_attivi[0], prenotazioni_attive=prenotazioni_attive[0], ultimi_prestiti=ultimi_prestiti, ultime_prenotazioni=ultime_prenotazioni)
