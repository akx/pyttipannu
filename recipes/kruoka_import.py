import re

import requests

from recipes.models import Recipe


def import_by_query(query):
    resp = requests.post(
        'https://www.k-ruoka.fi/kr-api/search/%s' % query,
        params={'offset': 0},
    )
    resp.raise_for_status()
    for recipe in resp.json()['result']:
        massaged = massage_kruoka_recipe(recipe)
        name = massaged.pop('name')
        massaged['public'] = True
        recipe, _ = Recipe.objects.update_or_create(name=name, defaults=massaged)
        yield recipe


def massage_kruoka_recipe(recipe):
    name = "%s \u2013 K-Ruoka" % recipe['Name']
    content = '%s\n\n%s' % (
        re.sub('^#\s+', '1. ', recipe['Instructions'], flags=re.MULTILINE),
        recipe['Url'],
    )
    return {
        'name': name,
        'content': content,
    }
