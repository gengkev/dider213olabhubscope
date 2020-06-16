import jwt
import requests

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.google import make_google_blueprint
from flask_login import LoginManager, login_user, logout_user

from . import config
from .models import db, User


login_manager = LoginManager()
login_manager.login_view = 'auth.login'

bp = Blueprint('auth', __name__)

google_bp = make_google_blueprint(
    scope=[
        'openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
    ],
    hosted_domain=config.REQUIRED_GOOGLE_DOMAIN,
)

github_bp = make_github_blueprint()


@bp.route('/login/')
def login():
    return render_template('auth/login.html')


@bp.route('/logout/')
def logout():
    logout_user()
    return render_template('auth/logout.html')


@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    if not token:
        flash('Failed to log in with Google.', category='error')
        return False

    # Get user info from Google servers
    # TODO: use the well-known URLs instead of hardcoding
    r = blueprint.session.get('/oauth2/v3/userinfo')
    user_info = r.json()

    # Extract fields from input
    google_id = user_info['sub']
    assert type(google_id) == str

    email = user_info['email']
    assert type(email) == str

    name = user_info.get('name', None)
    assert type(name) == str or name is None

    email_verified = user_info['email_verified']
    assert type(email_verified) == bool

    hd = user_info['hd']
    assert type(hd) == str

    # Ensure that the user verified their email
    if not email_verified:
        flash('Email is not verified.', category='error')
        return False

    # Verify that domain is correct
    if hd != config.REQUIRED_GOOGLE_DOMAIN:
        flash('Cannot sign in with the provided account.', category='error')
        return False

    # Extract username from email
    assert email.endswith(config.EMAIL_SUFFIX)
    username = email[:-len(config.EMAIL_SUFFIX)]

    # Search for existing user
    user = User.query.filter_by(google_id=google_id).first()
    if user is None:
        # Create a new user
        user = User(
            google_id=google_id,
            username=username,
            name=name,
        )
        db.session.add(user)
        db.session.commit()

    else:
        # Check if we need to update existing user
        if user.username != username:
            user.username = username
        if user.name != name:
            user.name = name
        db.session.commit()


    # Mark as signed-in in session
    res = login_user(user)
    assert res
    flash('Successfully signed in as {}.'.format(username))

    # Disable default behavior of flask-dance
    return False


@oauth_authorized.connect_via(github_bp)
def github_logged_in(blueprint, token):
    if not token:
        flash('Failed to log in with GitHub.', category='error')
        return False

    resp = blueprint.session.get('/user')
    if not resp.ok:
        flash('Failed to fetch user info from GitHub.', category='error')
        return False

    github_info = resp.json()
    github_user_id = github_info['id']
    github_username = github_info['login']
    flash('Signed into GitHub as user {} / {}.'.format(
        github_user_id, github_username))
    print(github_info)

    return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
