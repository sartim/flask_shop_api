# Flask Shop API

REST API which exposes endpoints both for an online shop and a CMS admin. It's developed using flask framework which runs as a socketio server. The database configuration for the app relies on PostgreSQL.

## Setup

**Requirements**

* Virtualenv
* Redis
* Heroku CLI


**Create virtual environment & install requirements**

    $ virtualenv <envname> -p python3
    $ source <envname>/bin/activate
    $ pip install -r requirements.txt

**Make migrations**

    $ python manage.py db init
    $ python manage.py db migrate
    $ python manage.py db upgrade

**Add dotenv to project root**

You should create a .env file on the project root using the following format:

    DEV=TRUE
    TEST=FALSE
    PROD=FALSE
    DATABASE_URL={DB_URL}
    SECRET_KEY={SECRET}
    PAGINATE_BY=20
    ADMIN_EMAIL={EMAIL}
    APP_EMAIL={EMAIL}
    APP_EMAIL_PASSWORD={PASSWORD}
    LOG_LEVEL=DEBUG


**Running app using heroku cli**

    $ heroku local web
    
**Running app using manage.py**

    $ python manage.py run server

**Running app using gunicorn**

    $ gunicorn --worker-class eventlet -w 1 wsgi:app

