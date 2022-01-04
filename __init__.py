from flask import Flask, render_template, url_for, redirect, g, make_response, send_file
from auth import login_required
from flask_qrcode import QRcode
import auth, db, Homepage, biblioteca
import db, mysql.connector

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'SuperSecretKey'
app.register_blueprint(auth.bp)
app.register_blueprint(Homepage.bp)
QRcode(app)
app.register_blueprint(biblioteca.bp)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


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

    cursor.close()
    dbconn.close()

    return render_template('user.html', user=g.user, num_lib=num_lib_prestito, num_prenotazioni=num_prenotazioni)


@app.route('/sw.js')
def sw():
    response = make_response(
        send_file('static/js/sw.js'))
    # change the content header file. Can also omit; flask will handle correctly.
    response.headers['Content-Type'] = 'application/javascript'
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
