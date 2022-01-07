from datetime import date, timedelta

from werkzeug.security import generate_password_hash, check_password_hash

import auth, db, Homepage
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
import mysql.connector

bp = Blueprint('biblioteca_admin', __name__)