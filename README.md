[![Tests](https://github.com/callat-qcd/lattedb/workflows/Tests/badge.svg)](https://github.com/callat-qcd/lattedb/actions)


# LatteDB

Lattice QCD database interface based on [EspressoDB](https://github.com/callat-qcd/espressodb).

## Description

## Install
Install via pip
```bash
pip install [--user] [-e] .
```

You must set up the `db-config.yaml` and `settings.yaml` file.
These files specify in which setup you want to use and how run the database connection.

For a general setup, take a look at the [EspressoDB documentation](https://espressodb.readthedocs.io/en/latest/Usage.html).

If you want to connect to a specific database, contact the admin of this instance.

## Run
After configuration you can launch a local server with
```bash
lattedb runserver
```
Or connect your scripts with LatteDB
```python
from lattedb.project.formfac.models import DiskConcatenatedFormFactor4DFile as DCFF4DF

files = DCFF4DF.objects.filter(exists=False)
print(files.count())
```

### Notes on testing
Run
```bash
pip install -r requirement-dev.txt
pytest
```
in the repo root to run the tests.


## Management interface
Go to the admin page [http://127.0.0.1:8000](http://127.0.0.1:8000) (once the server is running.)
Note that the address might change (look at the output of `lattedb runserver`).

## Authors
* [@cchang5](https://github.com/cchang5)
* [@ckoerber](https://github.com/ckoerber)

## Contribute
To be discussed...

### git workflow
* New features should be added to `devel-{feature}`, and will be merged into `master` once they work
* Developers should add tests for new features and make sure **all tests** don't fail before running `migrate` and `push`
* All `migrated` changes must be pushed to master
