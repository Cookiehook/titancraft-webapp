import base64
import logging
import os
from copy import copy
from urllib.parse import urlencode

import boto3

from app.models.locations import Location, Maintainer

logger = logging.getLogger()
PAGINATION = 25


def get_secret(secret_name):
    # Used when running on developer machine
    if secret := os.getenv(secret_name):
        logger.info(f"Retrieving {secret_name} secret from env vars")
        return secret

    # Used when running inside docker-compose network
    if os.path.exists(f"/run/secrets/{secret_name}"):
        logger.info(f"Retrieving {secret_name} secret from secret file")
        with open(f"/run/secrets/{secret_name}") as sfile:
            return sfile.read()

    # Used when deployed to AWS
    logger.info(f"Retrieving {secret_name} secret from secret manager")
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="eu-west-2"
    )

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    logger.debug(f"Secret '{secret_name}' = {get_secret_value_response}")
    if 'SecretString' in get_secret_value_response:
        return get_secret_value_response['SecretString']
    else:
        return base64.b64decode(get_secret_value_response['SecretBinary'])


def is_maintainer(user, **kwargs):
    location = Location.objects.get(**kwargs)
    maintainers = Maintainer.objects.filter(location=location)
    return user.is_staff or user in [m.user for m in maintainers]


def set_pagination_details(in_query, iterable, current_page, context):
    query = copy(in_query)
    if 'page' in query:
        del query['page']
    context['query'] = urlencode(query)
    if len(iterable) == PAGINATION:
        context["next_page"] = current_page + 1
    if current_page > 0:
        context['previous_page'] = current_page - 1
