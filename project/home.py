from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required, current_user
from flask_wtf import FlaskForm

from .models import Course, CourseUser


bp = Blueprint('home', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('home/index.html')


@bp.route('/profile')
def profile():
    return render_template(
        'home/profile.html',
         now=datetime.utcnow(),
    )


@bp.route('/protected', methods=('GET',))
@login_required
def protected():
    user = flask_login.current_user
    return 'Logged in as: ' + user.id
