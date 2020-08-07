lattedb test
lattedb migrate
lattedb collectstatic --noinput
lattedb check --deploy

# Prepare log files and start outputting logs to stdout
touch gunicorn.log
touch access.log

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn lattedb.config.wsgi:application \
    --name lattedb \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    --log-file=gunicorn.log \
    --access-logfile=access.log \
    "$@"
