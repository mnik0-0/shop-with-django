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
First create new **virtualenv**
```
virtualenv your-virtualenv
```
Than activate it with
```
. ./your-virtualenv/bin/activate
```
Finally, go to project directory and run
```
pip install -r requirements.txt
```

#### Create Database for project
```
sudo -u postgres psql
```
```
CREATE DATABASE test
CREATE USER test with encrypted password 'test'
GRANT ALL PRIVILEGES ON DATABASE test TO test;
ALTER USER test createdb;
```

### Setup django-environ
Now you need to create **.env** file near **manage.py**
```
DEBUG=on
SECRET_KEY="secret"
DATABASE_URL=psql://test:test@127.0.0.1:5432/test
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
### Testing
To test  project just use
```
python3 manage.py test
```
***
