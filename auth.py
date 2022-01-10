import functools
import string, random
import sys
import db, mysql.connector, re
from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, make_response
)

from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
user = None


def checkemail(email):
    # pass the regular expression
    # and the string into the fullmatch() method
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def checkpw(password, conf_password):
    if password == conf_password:
        return True
    else:
        return False


def checkbirthdate(birthdate):
    if birthdate >= datetime.today().strftime('%Y-%m-%d'):
        return False
    else:
        return True


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['nome']
        cognome = nome = request.form['cognome']
        cf = request.form['cf']
        email = request.form['email']
        datanascita = request.form['data_di_nascita']
        citta = request.form['citta']
        nazione = request.form['nazione']
        password = request.form['password']
        conf_pw = request.form['conf_password']

        error = None

        if not checkemail(email):
            error = "Email non valida"

        if not checkpw(password, conf_pw):
            error = "Password non corrispondenti"
            print(error)

        if not checkbirthdate(datanascita):
            error = "Data nascita non valida"
            print(error)

        if error is None:
            password = generate_password_hash(password)
            token = get_random_string(64)
            dbconn = mysql.connector.connect(**db.get_config())
            cursor = dbconn.cursor()

            register_user = ("INSERT INTO UTENTE "
                             "(nome_ut, cognome_ut, email, CF, data_nascita, PW, citta_ut, token_ut)"
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

            data = (name, cognome, email, cf, datanascita, password, citta, token)

            cursor.execute(register_user, data)

            cursor.close()
            dbconn.commit()
            dbconn.close()

            return render_template('auth/registrazione_end.html')
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            error = 'L''username è richiesta'
        elif not password:
            error = 'La password è richiesta.'
        else:

            dbconn = mysql.connector.connect(**db.get_config())

            query = (
                "SELECT * FROM `UTENTE` WHERE email=%s"
            )

            cursor = dbconn.cursor()
            cursor.execute(query, (username,))

            user = cursor.fetchone()
            print(user)

            cursor.close()
            dbconn.close()

            if user is None:
                error = 'loginerror'

            elif not check_password_hash(user[6], password):
                error = 'loginerror'

            if error is None:
                session.clear()
                session['CF'] = user[3]

                if user[10] is not None:
                    return redirect(url_for('home.dashboard'))
                else:
                    return redirect(url_for('home.index'))

    if g.user is None:
        return render_template('auth/login.html', err=error)
    else:
        return redirect(url_for('home.index'))


# Funzione eseguita prima di qualsiasi richiesta
@bp.before_app_request
def load_logged_in_user():
    user_cf = session.get(
        'CF')  # Controllo che vi sia già un utente loggato attraverso la funzione session.get la quale mi restituirà il CF se è loggato / None se non è loggato

    if user_cf is None:  # Se ho avuto None --> g.user sarà = None
        g.user = None
    else:
        dbconn = mysql.connector.connect(
            **db.get_config())  # Se ho avuto il CF dell'utente vado a prelevarmi i dati dal DB  dell'utente con quel CF e a metterli in g.user
        cursor = dbconn.cursor()
        query = 'SELECT * FROM UTENTE WHERE CF = %s'
        cursor.execute(query, (user_cf,))
        g.user = cursor.fetchone()
        print(g.user)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user[10] is None:
            return redirect(url_for('home.index'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/reimpostapw', methods=('GET', 'POST'))
@login_required
def reimposta_pw():
    if request.method == 'POST':
        vecchia_pw = request.form['vecchia-pw']
        nuova_pw = request.form['nuova-pw']
        nuova_pw_2 = request.form['nuova-pw2']

        error = None

        if not check_password_hash(g.user[6], vecchia_pw):
            error = 'oldpass_false'
            return jsonify(status='ErrorOldPW')

        if nuova_pw != nuova_pw_2:
            error = 'Password non corrispondenti'
            return jsonify(status='ErrorNewPW')

        if error is None:
            dbconn = mysql.connector.connect(**db.get_config())
            cursor = dbconn.cursor()
            q_change_pw = ('UPDATE UTENTE SET PW=%s WHERE EMAIL = %s')
            cursor.execute(q_change_pw, (generate_password_hash(nuova_pw), g.user[2]))

            dbconn.commit()
            cursor.close()
            dbconn.close()

            return jsonify(status='Success')


@bp.route('/richiediregistrazione', methods=('GET', 'POST'))
def richiedi_registrazione_biblioteca():

    inviato = False

    if request.method == 'POST':
        nome_biblioteca = request.form['nomebib']
        indirizzo_biblioteca = request.form['indirizzobib']
        numero_tel_biblioteca = request.form['numtelbib']

        nome_titolare = request.form['nometitolare']
        cognome_titolare = request.form['cognometitolare']
        email_titolare = request.form['emailtitolare']
        numero_tel_titolare = request.form['numteltitolare']
        data_di_nascita_titolare = request.form['datadinascita']
        citta_titolare = request.form['citta']
        nazione_titolare = request.form['nazione']

        inviato = True

        return render_template('auth/register_biblioteca.html', inviato=inviato)

    return render_template('auth/register_biblioteca.html', inviato=inviato)
