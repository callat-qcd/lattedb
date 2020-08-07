#!/bin/sh -l
set -e

echo "Starting entrypoint."

pytest -x $LATTEDB_APP_DIR
lattedb migrate
lattedb collectstatic --noinput
lattedb check --deploy

# Start server
lattedb runserver 0.0.0.0:8000
