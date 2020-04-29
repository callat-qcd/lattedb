# Load in python image
FROM python:3.7-buster

# Create dirs
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/.pip_cache

# Set workdir
WORKDIR /opt/app

# Install requirements
COPY requirements.txt /opt/app
RUN pip install --upgrade pip --cache-dir /opt/app/.pip_cache
RUN pip install -r requirements.txt --cache-dir /opt/app/.pip_cache

# Install lattedb
# DO NOT COPY PRIVATE FILES LIKE db-config.yaml or settings.yaml
# These will be served privately
COPY setup.py /opt/app/
COPY README.md /opt/app/
COPY MANIFEST.in /opt/app/
COPY lattedb /opt/app/lattedb
RUN pip install . --cache-dir /opt/app/.pip_cache
