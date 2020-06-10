import os
import requests

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
SERVER_NAME = os.getenv('SERVER_NAME')

# SQLAlchemy database config
SQLALCHEMY_DATABASE_URI = 'sqlite:///{instance_path}/test.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Google OAuth config
GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

# GitHub OAuth config
GITHUB_OAUTH_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_OAUTH_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')

# Tell Google OAuth to force sign-in with this domain
REQUIRED_GOOGLE_DOMAIN = 'andrew.cmu.edu'

# Required suffix to strip from all email addresses
EMAIL_SUFFIX = '@' + REQUIRED_GOOGLE_DOMAIN
