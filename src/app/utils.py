import base64
import logging
import os
from copy import copy
from functools import reduce
from urllib.parse import urlencode

import boto3
from django.db.models import Q

from app.models.constants import Item, ItemClass
from app.models.stock import FarmRecord

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


def set_pagination_details(in_query, iterable, current_page, context):
    query = copy(in_query)
    if 'page' in query:
        del query['page']
    context['query'] = urlencode(query)
    if len(iterable) == PAGINATION:
        context["next_page"] = current_page + 1
    if current_page > 0:
        context['previous_page'] = current_page - 1


def get_farms_for_locations(locations, user):
    all_farms = {}
    for location in locations:
        if all_farms.get(location) is None:
            location.set_display_data(user)
            all_farms[location] = []
        farm_records = FarmRecord.objects.filter(location=location).order_by("location", "mob", "item")
        [f.set_display_data(user) for f in farm_records]
        all_farms[location] = [f.view_data for f in farm_records]
    return all_farms


def search_item(search_term):
    """
    In order, search for items that:
      Name exactly matches the search term
      Name contains the search term (excluding already found)
      Name contains a word from the search term (excluding already found)
      Items in the same class as exact or close matches
      Class contains a word from the search term (excluding already found)

    :param search_term:
    :return: List of item groups, in decreasing relevance
    """
    any_word_query = reduce(lambda q, f: q | Q(name__icontains=f), search_term.split(), Q())
    match_exact_items = Item.objects.filter(name__iexact=search_term).all()
    match_close_items = Item.objects.filter(name__icontains=search_term).exclude(id__in=match_exact_items).all()
    match_single_word_items = Item.objects.filter(Q(any_word_query & ~Q(id__in=match_exact_items | match_close_items)))
    classes = ItemClass.objects.filter(item__in=match_exact_items | match_close_items)
    match_class_items = [i.item for i in ItemClass.objects.filter(
        Q(Q(name__in=classes.values('name')) &
          ~Q(item__in=match_exact_items | match_close_items | match_single_word_items)))]
    match_class_name_items = [i.item for i in ItemClass.objects.filter(
        Q(any_word_query & ~Q(item__in=match_exact_items | match_close_items | match_single_word_items)))]

    return match_exact_items, match_close_items, match_single_word_items, match_class_items, match_class_name_items
