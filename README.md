## Phonebook
### Preparing
Before running django project you must first create virtualenv.

``` shell
$ python3.9 -m pip install virtualenv
$ python3.9 -m virtualenv venv
```

To activate virtual environment in ubuntu:
```shell
$ source venv\bin\activate
```

To deactivate environment use:
``` shell
$ deactivate
```

After activation must install all packages:
```shell
$ pip install -r requirements.txt
```
### Run project
1. Config setting from ***settings-template.ini***

2. Generate jwt RSA keys (without passphrase)
```bash
$ ssh-keygen -t rsa -b 4096 -m PEM -f jwt-key
$ openssl rsa -in jwt-key -pubout -outform PEM -out jwt-key.pub
```
3. Create postgres db
``` sql
CREATE USER <user> WITH PASSWORD <password>;
CREATE DATABASE <db>;
ALTER ROLE <user> SET client_encoding TO 'utf8';
ALTER ROLE <user> SET default_transaction_isolation TO 'read committed';
ALTER ROLE <user> SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE <db> TO <user>;
```
4. To create all database tables:
```shell
$ python manage.py makemigrations
$ python manage.py migrate
```

5. Deployment Check
```shell
$ python manage.py collectstatic
$ python manage.py check
$ python manage.py test
$ python manage.py check --deploy
```

6. Now you can run project using these commands
```bash
# simple django server
$ python manage.py runserver

# gunicorn (if you have conf.py in config/gunicorn) 
$ gunicorn -c config/gunicorn/conf.py --preload --bind :8000 --chdir kernel kernel.wsgi:application
```

NOTE: If **psycopg2** doesn't install in ubuntu OS:
```sh
$ pip install psycopg2-binary
```