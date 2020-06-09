# dider213olabhubscope

Installation:

    $ python3 -m pip install poetry
    $ poetry install

Running development server:

    $ export FLASK_APP=project
    $ export FLASK_ENV=development
    $ poetry run flask run

Initializing database tables:

    $ poetry run flask db upgrade
