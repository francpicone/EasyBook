from flask import Flask, render_template, url_for, redirect, g
import auth, db
import db

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'SuperSecretKey'
app.register_blueprint(auth.bp)


@app.route('/')
def index():
    if g.user is not None:      #Se g.user non è nullo, quindi ho un utente loggato, reindirizzo il browser alla homapage
        print(g.user)
        return render_template('homepage.html')
    else:                       #Diversamente, se g.user è None, quindi non ho un utente loggato, reindirizzo il browser alla pagina di login
        return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
