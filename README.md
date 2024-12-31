# Yu-Gi-Oh API

## Previous knowledge
<!-- UL -->
1. [Git](https://github.com/)
2. [Python](https://www.python.org/)
3. [Django](https://www.djangoproject.com/)

## Getting started

Follow the steps below to install the app in your corresponding environment

## Download the repository via git

```
# Clone git repo in your path
git clone https://github.com/elMauro2003/yugioh-api.git
      
```

## Development environment 

Create your virtual env 

```
Example:
python -m venv env    
```
Linux Run env
```
source env/bin/activate
```

Windows Run env
```
env\Scripts\activate
```


## Install the project requirements

>Run next comand 
```
pip install -r requirements.txt
```


## Configure .env file with environment variables


Create your .env and configure it if you use production environment. 

Run db.sqlite3 by default

```
USE_DB = <sqlite3>                          # if you use postgres change sqlite for postgres and configure the other db parameters

# use this configuration if you prefer postgres
ENGINE = <your db engine>                   # default django.db.backends.postgresql
DB_NAME = <your db name>                    # default postgres
DB_USER = <your db user>                    # default postgres
DB_PASSWORD = <your db password>            # default postgres
DB_HOST = <your db host>                    # default 127.0.0.1
DB_PORT = <your db port>                    # default 5432

# optional valriables
DJANGO_SETTINGS_MODULE=< your settings configuration > # default 'sinfimac.settings.production'
SECRET_KEY= <your secret key>
DEBUG = <True>                              # default False in production
TIME_ZONE = <your time zone>                # default UTC
LANGUAGE_CODE= <your lenguage>              # default en-us

```




## Run migrations

```python
python manage.py migrate
```

## If you want to create a super user
##### Remember to enter real emails so that the task editing messages can reach multiple users.

```python
python manage.py createsuperuser
```


## Run server

```python
python manage.py runserver
```
