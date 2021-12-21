from flask import Flask, render_template, url_for, redirect, g
from auth import login_required
from flask_qrcode import QRcode
import auth, db, Homepage
import db

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'SuperSecretKey'
app.register_blueprint(auth.bp)
app.register_blueprint(Homepage.bp)
QRcode(app)


@app.route('/utente')
@login_required
def get_profile():
    return render_template('user.html', user=g.user)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
