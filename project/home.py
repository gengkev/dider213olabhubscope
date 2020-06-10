from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required


bp = Blueprint('home', __name__)


@bp.route('/', methods=('GET',))
def index():
    return render_template('index.html')


@bp.route('/bla', methods=('GET',))
def bla():
    return 'hello: ' + url_for('google.login')


@bp.route('/protected', methods=('GET',))
@login_required
def protected():
    user = flask_login.current_user
    return 'Logged in as: ' + user.id
