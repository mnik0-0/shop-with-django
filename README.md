# Shop with Django

[![Build Status](https://travis-ci.org/mnik0-0/shop-with-django.svg?branch=master)](https://travis-ci.org/github/mnik0-0/shop-with-django)

##### It' s the online store, where everyone can put their goods for sale.
***
## In development process. 
Now in settings you can see that 

```
DEBUG = True
```
***
# Running Locally

### Clone the project
```
git clone https://github.com/mnik0-0/shop-with-django
```

### Install requirements.txt 
Go to project directory and run
```
pip install -r requirements.txt
```

### Create and connect Database
##### I use Postgresql in this project
##### So by default in settings you an see
```
    'NAME': 'travisdb',
    'USER': 'postgres',
    'PASSWORD': '',
```
##### But I reccomend you to replace it with 
```
    'NAME': 'your_database',
    'USER': 'your_username',
    'PASSWORD': 'your_password',
    'HOST': '127.0.0.1',
    'PORT': '5432', #default port
```
##### Than
```
sudo -u postgres psql
```
```
CREATE DATABASE your_database;
CREATE USER your_username WITH password 'your_password';
GRANT ALL ON DATABASE your_database TO your_username;
```

##### And finaly you will need to make migrations
```
python3 manage.py makemigrations
python3 manage.py migrate
```
***
## You are ready to run your local server
```
python3 manage.py runsever
```
***
