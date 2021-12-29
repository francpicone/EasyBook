from flask import Flask, render_template, url_for, redirect, g
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


@app.route('/utente')
@login_required
def get_profile():

    dbconn = mysql.connector.connect(**db.get_config())
    cursor = dbconn.cursor()
    q_get_num_libri_prestito = ('select count(num_copia) as libri_presi from COPIA_LIBRO join PRENDE_IN_PRESTITO on num_copia=num_copia_prestito join UTENTE on PRENDE_IN_PRESTITO.codice_fiscale=UTENTE.cf WHERE CF = %s GROUP BY CF')
    cursor.execute(q_get_num_libri_prestito, (g.user[3], ))
    num_lib_prestito = cursor.fetchone()

    return render_template('user.html', user=g.user, num_lib=num_lib_prestito)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
