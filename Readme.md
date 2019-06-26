# LatteDB

Lattice QCD database interface using [Django](https://docs.djangoproject.com/en/2.2/intro/tutorial01/) as the content manager.

## Description

## Install
Install via pip
```bash
pip install [--user] [-e] .
```

## Run
1. If you start the app for the first time you must configure the database setup file `db-config.yaml`.
An example file is given by `postgres-example.yaml`. Simply adjust and copy this to `db-config.yaml`.
See also [connecting-to-the-database](https://docs.djangoproject.com/en/2.2/ref/databases/#connecting-to-the-database).

2. Next, you must create the database by running
```
python manage.py makemigrations # this prepares sql
python manage.py migrate   # this is sql
```
This step must be repeated each time you change tables.

3. Create a super user:
```
python manage.py createsuperuser
```

4. The following command in your bash to initiate an interactive server
```
python manage.py runserver
```

You can access the interface in your browser.

## Development
Table schemas are implemented in `base.modeles`.
See also [the Django model doc](https://docs.djangoproject.com/en/2.2/topics/db/models/).

## Management interface
Go to the admin page [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) (once the server is running.)
Note that the address might change (look at the output of `manage.py runserver`).

## Authors
* [@cchang5](https://github.com/cchang5)
* [@ckoerber](https://github.com/ckoerber)

## Contribute
To be discussed...
