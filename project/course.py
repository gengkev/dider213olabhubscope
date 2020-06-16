from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required, current_user
from functools import wraps
from werkzeug.exceptions import Forbidden
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import Course, CourseUser, ModelForm, User, UserType


bp = Blueprint('course', __name__)


@bp.url_defaults
def add_course_code(endpoint, values):
    '''Provides a default course code when calling url_for().'''
    if hasattr(g, 'course_code'):
        values.setdefault('course_code', g.course_code)


@bp.url_value_preprocessor
def pull_course_code(endpoint, values):
    '''Sets the course code based on the URL prefix.'''
    g.course_code = values.pop('course_code')
    g.course = Course.query.filter_by(code=g.course_code).first()
    g.course_user = None
    if g.course is not None:
        g.course_user = CourseUser.query.filter_by(
            course_id=g.course.id,
            user_id=current_user.id,
        ).first()


def course_user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.course_user is None:
            raise Forbidden('You are not enrolled in this course.')
        return f(*args, **kwargs)
    return decorated_function


def course_instructor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (g.course_user is None or
                g.course_user.user_type != UserType.INSTRUCTOR):
            raise Forbidden('You are not an instructor in this course.')
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/')
@login_required
def index():
    return render_template('course/index.html')


@bp.route('/users/')
@login_required
@course_instructor_required
def users():
    return render_template('course/users.html')


class UserCreateForm(ModelForm):
    user = QuerySelectField()
    class Meta:
        model = CourseUser
        include_foreign_keys = True


@bp.route('/users/create/')
@login_required
@course_instructor_required
def users_create():
    form = UserCreateForm()
    form.user.query = User.query
    return render_template(
        'course/users_create.html',
        form=form,
    )
