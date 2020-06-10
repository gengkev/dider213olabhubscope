import jwt
import requests

from flask import flash
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.google import make_google_blueprint
from flask_login import LoginManager, login_user

from . import config
from .models import db, User


login_manager = LoginManager()

google_bp = make_google_blueprint(
    scope=['openid', 'https://www.googleapis.com/auth/userinfo.email'],
    hosted_domain=config.REQUIRED_GOOGLE_DOMAIN,
)

github_bp = make_github_blueprint()


@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    if not token:
        flash('Failed to log in with Google.', category='error')
        return False

    # Parse id_token instead of making a separate userinfo request
    # Token comes from Google servers, so don't bother to verify signature
    id_token = jwt.decode(
        token['id_token'],
        audience=config.GOOGLE_OAUTH_CLIENT_ID,
        options=dict(verify_signature=False),
    )

    if not id_token['email_verified']:
        flash('Email is not verified.', category='error')
        return False

    # Verify that domain is correct
    if id_token['hd'] != config.REQUIRED_GOOGLE_DOMAIN:
        flash('Cannot sign in with the provided account.', category='error')
        return False

    google_email = id_token['sub']
    email = id_token['email']
    print(id_token)

    # Extract username from email
    assert email.endswith(config.EMAIL_SUFFIX)
    username = email[:-len(config.EMAIL_SUFFIX)]

    # Search for existing user
    user = User.query.filter_by(username=username).first()
    if user is None:
        # Create a new user
        user = User(username=username)
        db.session.add(user)
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
