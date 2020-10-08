Yes, the PR #42 implements this. Notes on how to use it are in the `how-to-use-local-dbs.md`:

# How to use local dbs

This file specifies how to create a local back up of `formfac.correlator` data.

## Setting up the local db

1. Work on the `feature-dual-db` branch
2. Work on a machine which has access to ithems
3. Make sure that `db-config.yaml` is set up such that you connect to the ithems postgres db
4. Create a new file `db-config-local.yaml` with the content (this will spawn the sqlite db for copying data back and forth)

```
ENGINE: django.db.backends.sqlite3
NAME: /path/to/local/file/db-name.sqlite
```

5. Migrate models to **new local db** (you should make sure that models are up to date (as in most recent commit). You can check this by running `python makemigrations`)

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
3. set up **`db-config.yaml` to the local config** (note this is a different setting than on the machine used for cloning)

```
ENGINE: django.db.backends.sqlite3
NAME: /remote/path/to/local/file/db-name.sqlite
```

4. Run scripts as before.

## Updating the default db

1. `rsync` the remote db `/remote/path/to/local/file/db-name.sqlite` back to your local machine (same place as before).
2. Backup the default db as usual (you don't want to screw up now)
3. Insert new data from the sql file back to the default db
```bash
python clone_corrs.py -u
```

This runs some checks and asks you if things make sense before continuing, still someone else may want to test this :)
