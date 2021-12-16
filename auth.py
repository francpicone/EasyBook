import functools
import sys
from flask_sqlalchemy import sqlalchemy as db

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None


        if username == 'pippo':
            return render_template('homepage.html')

    return render_template('auth/login.html')
