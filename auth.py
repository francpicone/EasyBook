import functools
import string, random
import sys
import db, mysql.connector, re
from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
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
        nome = request.form['nome']
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

            data = (nome, cognome, email, cf, datanascita, password, citta, token)

            cursor.execute(register_user, data)

            cursor.close()
            dbconn.commit()
            dbconn.close()

            return render_template('auth/registrazione_end.html')
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

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

            if user is None:
                error = 'Username non corretta'
            elif not check_password_hash(user[6], password):
                error = 'Password non corretta'

            if error is None:
                session.clear()
                session['CF'] = user[3]
                return redirect(url_for('home.index'))

            flash(error)

            cursor.close()
            dbconn.close()

    return render_template('auth/login.html')


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
