from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required, current_user


bp = Blueprint('home', __name__)


@bp.route('/', methods=('GET',))
def index():
    return render_template('index.html')


@bp.route('/bla', methods=('GET',))
def bla():
    print(current_user)
    return 'hello: {}'.format(current_user.is_authenticated)


@bp.route('/protected', methods=('GET',))
@login_required
def protected():
    user = flask_login.current_user
    return 'Logged in as: ' + user.id
