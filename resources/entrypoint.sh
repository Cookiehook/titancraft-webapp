#!/bin/bash
export DJANGO_SETTINGS_MODULE="project.settings_prod"
pipenv run python manage.py migrate
pipenv run supervisord -c /app/supervisor.conf
