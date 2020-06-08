from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET',))
def login():
    return render_template('auth/login.html')
