# HealthBuddy

## Getting started

### Set environment variable
Create a file called `.env` at the root of the project and assign the following variables:

- `DEBUG`: Enable/disable the debug mode. 
    - Development Default: `True`
    - Production: `False`
- `SECRET_KEY`: Secret key used to cryptographic reasons;
    - Development Default: `k+n)wd-p=iuwicmwmx1vb^suptfaz#u+g1%c!2pa9s-)c=#xz7`
    - Required in production;

### Installing the dependencies
- Python 3.6+
- PostgreSQL 10.12+

### Create and active virtualenv
```shell script
$ python3 -m venv env
$ source env/bin/activate
```
#### Install requirements
```shell script
$ pip install -r requirements.txt
or
$ pip install -r requirements-dev.txt
```
#### Run the migrations
```shell script
$ cd gestotus
$ python manage.py makemigrations
$ python manage.py migrate
```
#### Now run project
```shell script
$ python manage.py runserver
```
