# Flask Shop API

[![Language](https://img.shields.io/badge/language-python-green.svg)](https://github.com/sartim/flask_shop_api)
![build](https://github.com/sartim/flask_shop_api/workflows/build/badge.svg)

REST API which exposes endpoints both for an online shop and a CMS admin. It's developed using flask framework which runs as a socketio server.

##Features

* RBAC
* API Caching (Redis)
* Fulltext search (Elasticsearch)

## Setup

**Requirements**

* Python 3+
* Virtualenv
* Heroku CLI


**Create virtual environment & install requirements**

    $ virtualenv <envname> -p python3
    $ source <envname>/bin/activate
    $ pip install -r requirements.txt --use-feature=2020-resolver 

**Make migrations**

    $ python manage.py db init
    $ python manage.py db migrate
    $ python manage.py db upgrade

**Add dotenv to project root**

You should create a .env file on the project root using the following format:

When using PostgreSQL DB_URL

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

When using sqlite for test

    DEV=FALSE
    TEST=TRUE
    PROD=FALSE
    SECRET_KEY=my_precious
    PAGINATE_BY=20
    ADMIN_EMAIL=admin@mail.com
    APP_EMAIL=app@email.com
    APP_EMAIL_PASSWORD=letmein
    LOG_LEVEL=DEBUG
    
**Running app using manage.py**

    $ python manage.py run

**Running app using gunicorn**

    $ gunicorn --worker-class eventlet -w 1 wsgi:app
    
**Building & running on docker**

    $ docker build --build-arg ENV=PROD --build-arg PAGINATE_BY=20 --build-arg CACHED_QUERY=CACHED_QUERY --build-arg REDIS_EXPIRE=3600 --build-arg SECRET_KEY=my_secret --build-arg REDIS_URL=redis://host:port --build-arg DATABASE_URL=postgresql://username:password@hostname:5432/database --build-arg ADMIN_EMAIL=test@mail.com --build-arg APP_EMAIL=test@email.com --build-arg APP_EMAIL_PASSWORD=password --build-arg LOG_LEVEL=ERROR -t flask-shop-api .
    $ docker run -p 5000:5000 flask-shop-api

**Running unittests**
    
First setup the .env for test environment then run the following command from project root:
    
    $ pytest

**Other Commands on** 

    python manage.py --help

_(Optional)Install Ipython to get interactive shell using Ipython for the app_


**Demo URL**

`https://flask-shop-api-git-develop-sartims-projects.vercel.app`

###### Login Credentials

username: `demo@mail.com`

password: `demo_pass`


###### Routes

* /api/v1/auth/generate-jwt
* /api/v1/users
* /api/v1/categories
* /api/v1/products
* /api/v1/statuses
* /api/v1/orders
* /api/v1/reviews
