from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required, current_user

from .models import Course, CourseUser


bp = Blueprint('home', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('home/index.html')


@bp.route('/course/<course_code>/')
@login_required
def course_detail(course_code):
    course = Course.query.filter_by(code=course_code).first()
    return render_template(
        'home/course_detail.html',
        course=course,
        my_course_user=None,
    )


@bp.route('/protected', methods=('GET',))
@login_required
def protected():
    user = flask_login.current_user
    return 'Logged in as: ' + user.id
