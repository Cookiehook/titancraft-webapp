FROM python:3.9

WORKDIR /app/
ENV LANG "en_US.UTF-8"
ENV PYTHONPATH .
ENV PYTHONUNBUFFERED 1
RUN mkdir /logs

# Install dependencies
RUN apt-get update && apt-get install -y nginx && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN pip install pipenv==2020.11.15
COPY Pipfile* /app/
RUN pipenv install --ignore-pipfile

# Copy in application code
COPY src /app/src/
COPY resources/* /app/

# Prepare environment
WORKDIR /app/src/
RUN pipenv run python manage.py collectstatic --no-input

ENTRYPOINT /app/entrypoint.sh
