from flask import Flask, render_template, g, make_response, send_file, jsonify, redirect, url_for
from flask_qrcode import QRcode
import Homepage
import auth
import biblioteca
import biblioteca_admin
import db
import mysql.connector
from auth import login_required

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'SuperSecretKey'

UPLOAD_FOLDER = 'static/resources'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.register_blueprint(auth.bp)
app.register_blueprint(Homepage.bp)
QRcode(app)
app.register_blueprint(biblioteca.bp)
app.register_blueprint(biblioteca_admin.bp)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(400)
def page_not_found(e):
    return render_template('400.html'), 400


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


db.initdb()


@app.route('/utente')
@login_required
def get_profile():
    dbconn = mysql.connector.connect(**db.get_config())
    cursor = dbconn.cursor()

    q_get_num_libri_prestito = (
        'select count(num_copia) as libri_presi from COPIA_LIBRO join PRENDE_IN_PRESTITO on num_copia=num_copia_prestito join UTENTE on PRENDE_IN_PRESTITO.codice_fiscale=UTENTE.cf WHERE CF = %s GROUP BY CF')
    cursor.execute(q_get_num_libri_prestito, (g.user[3],))
    num_lib_prestito = cursor.fetchone()

    q_get_num_prenotazioni = (
        'SELECT COUNT(Id_prenotazione) FROM PRENOTAZIONI_POSTO JOIN UTENTE ON Utente = UTENTE.CF WHERE UTENTE.CF = %s')
    cursor.execute(q_get_num_prenotazioni, (g.user[3],))
    num_prenotazioni = cursor.fetchone()

    if g.user[10] is not None:
        q_get_num_posti_aula = 'SELECT Posti_aula_studio FROM BIBLIOTECA WHERE Id_biblioteca = %s'
        cursor.execute(q_get_num_posti_aula, (g.user[10],))
        num_posti_aula = cursor.fetchone()
        num_posti_aula = num_posti_aula[0]
    else:
        num_posti_aula = 0

    cursor.close()
    dbconn.close()

    return render_template('user.html', user=g.user, num_lib=num_lib_prestito, num_prenotazioni=num_prenotazioni,
                           num_posti_aula=num_posti_aula, rank=biblioteca.rank_calculator())


@app.route('/sw.js')
def sw():
    response = make_response(
        send_file('static/js/sw.js'))
    # change the content header file. Can also omit; flask will handle correctly.
    response.headers['Content-Type'] = 'application/javascript'
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
