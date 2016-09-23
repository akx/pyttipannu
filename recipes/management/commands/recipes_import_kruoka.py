from django.core.management import BaseCommand

from recipes.kruoka_import import import_by_query


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('query')

    def handle(self, query, **kwargs):
        for recipe in import_by_query(query):
            print(recipe.id, recipe)
