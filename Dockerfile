# Load in python image
FROM python:3.7-buster

# Who to contact
MAINTAINER Christopher Körber

# Environment variables and dirs used
## This stores app configs and static files (it should already exist)
ENV LATTEDB_ROOT_DIR=/www
## This is where the python app will be installed
ENV LATTEDB_APP_DIR=/opt/app
## This is the dir where work will happen (e.g., you can find logs)
ENV LATTEDB_WORK_DIR=/lattedb

# Create dirs
RUN mkdir -p $LATTEDB_APP_DIR
RUN mkdir -p $LATTEDB_APP_DIR/.pip_cache
RUN mkdir -p $LATTEDB_WORK_DIR

# Set workdir
WORKDIR $LATTEDB_APP_DIR

# Install requirements
COPY requirements.txt $LATTEDB_APP_DIR
RUN pip install --upgrade pip --cache-dir $LATTEDB_APP_DIR/.pip_cache
RUN pip install -r requirements.txt --cache-dir $LATTEDB_APP_DIR/.pip_cache

# Install lattedb
# DO NOT COPY PRIVATE FILES LIKE db-config.yaml or settings.yaml
# These will be served privately
COPY setup.py $LATTEDB_APP_DIR
COPY README.md $LATTEDB_APP_DIR
COPY MANIFEST.in $LATTEDB_APP_DIR
COPY lattedb $LATTEDB_APP_DIR/lattedb
RUN pip install . --cache-dir $LATTEDB_APP_DIR/.pip_cache

# Port to expose
EXPOSE 8000

# Copy entrypoint script into the image
## Check if tests pass
RUN lattedb test
WORKDIR $LATTEDB_WORK_DIR
COPY ./docker-entrypoint.sh .
ENTRYPOINT ["/docker-entrypoint.sh"]
