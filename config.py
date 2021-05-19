import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:<password>@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = False 
# SQLALCHEMY_ECHO = True
WTF_CSRF_ENABLED = False

# If you give error: ERROR [flask_migrate] Error: Target database is not up to date when yo connecting your local database using flask migrate try this commands:
# flask db stamp head
# flask db migrate
# flask db upgrade