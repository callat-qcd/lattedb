
# Setting up lattedb for the first time

1. Check out branch of choice
```bash
git checkout feature-spec4D-views && git pull
```

2. (Optional) Create new virtual environment
```bash
pip install --upgrade virtualenvwrapper
# Configure: https://virtualenvwrapper.readthedocs.io/en/latest/install.html
mkvirtualenv lattedb
```

3. Install `lattedb`
Because you want to use `postgres`, we have to make sure `psycopg2` is available:

a. Install postgres
```bash
brew install postgresql
pg_config # To test it works
```
b. Install lattedb
```bash
pip install -e .
```

4. Configure `lattedb`
a. Create the settings file which specifies Django details: Download https://github.com/callat-qcd/lattedb-wiki/blob/master/private_files/settings.yaml into the repo root. This file must not be committed to the main repo.

b. Create the db-settings file: Download https://github.com/callat-qcd/lattedb-wiki/blob/master/private_files/db-config-latte-master.yaml into the repo root and name it `db-config.yaml`. This file must not be committed to the main repo.

To check:
```bash
lattedb info
espressodb version: 1.2.0
DB access:admin@lattedb-ithems
```

## Use your own DB

This file is set up such that you access ithems.
You can also run a local copy/different db.

See also: https://wiki.postgresql.org/wiki/Homebrew

1. Start the database server



```psql
CREATE DATABASE lattedb;
```

# Setting up lattedb for the first time
