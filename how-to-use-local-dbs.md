# How to use local dbs

This file specifies how to create a local back up of `formfac.correlator` data.

## Setting up the local db

1. Work on the `feature-dual-db` branch
2. Work on a machine which has access to ithems
3. Make sure that `db-config.yaml` is set up such that you connect to ithems
4. Create a new file `db-config-local.yaml` with the content

```
ENGINE: django.db.backends.sqlite3
NAME: /path/to/local/file/db-name.sqlite
```

5. Migrate models to new local db (you should make sure that models are up to date before `python makemigrations`)

```bash
lattedb migrate --database=local
```

6. Clone the correlator data to the local db.
```bash
python clone_corrs.py -n
```

Done. You can now copy this file to any new machine and work with it.

## Using the local file on a remote machine

1. `rsync` the local db `/path/to/local/file/db-name.sqlite` to your remote machine.
2. Make sure lattedb is up to date
3. set up **`db-config.yaml`** to the local config (note this is a different setting than on the machine used for cloning)

```
ENGINE: django.db.backends.sqlite3
NAME: /path/to/local/file/db-name.sqlite
```

4. Run scripts as before.
