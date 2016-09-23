from django.core.management import BaseCommand
from django.db.transaction import atomic

from recipes.factories import RecipeFactory


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-n', '--count', default=500)

    @atomic
    def handle(self, count, **kwargs):
        for x in range(count):
            recipe = RecipeFactory(public=True)
            print(x + 1, recipe.id, recipe)
