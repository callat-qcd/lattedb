[![Tests](https://github.com/callat-qcd/lattedb/workflows/Tests/badge.svg)](https://github.com/callat-qcd/lattedb/actions)


# LatteDB

LatteDB, an application (Python) of [EspressoDB](https://github.com/callat-qcd/espressodb) that is specialized to contain table definitions for lattice quantum chromodynamics (LQCD) calculations and analysis.

The main page of ``LatteDB`` is hosted on [https://ithems.lbl.gov/lattedb](https://ithems.lbl.gov/lattedb).

## Install
Clone the repo and install via pip
```bash
pip install [--user] [-e] .
```

You must set up the `db-config.yaml` and `settings.yaml` file.
These files specify in which setup you want to use and how run the database connection.

For a general setup, take a look at the [EspressoDB documentation](https://espressodb.readthedocs.io/en/latest/Usage.html).

If you want to connect to a specific database, contact the admin of this instance.

## Test the install
Run
```pash
pip install -r requirements-dev.txt
pytest
```
in the repo root to run the tests.

## Usage

### Host a local webpage
After configuration you can launch a local server with
```bash
lattedb runserver
```
and visit [http://127.0.0.1:8000](http://127.0.0.1:8000) (once the server is running.)
Note that the address might change (look at the output of `lattedb runserver`).

### Import in Python
Or connect your scripts with LatteDB
```python
from lattedb.project.formfac.models import DiskConcatenatedFormFactor4DFile as DCFF4DF

files = DCFF4DF.objects.filter(exists=False)
print(files.count())
```

## Authors
* [@cchang5](https://github.com/cchang5)
* [@ckoerber](https://www.ckoerber.com)
