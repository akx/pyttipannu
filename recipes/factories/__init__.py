import os
from datetime import datetime
import random

from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from factory.django import DjangoModelFactory
from factory import fuzzy, Faker, post_generation
from faker.factory import Factory

fk = Factory.create()

from recipes.models import Recipe, RecipeRating

with open(os.path.join(os.path.dirname(__file__), 'foods.txt'), 'r', encoding='utf-8') as infp:
    INGREDIENTS = sorted(infp.read().strip().splitlines())

METHODS = [
    'boiled',
    'cooked',
    'deep-fried',
    'fried',
    'mashed',
    'massaged',
    'sautéed',
]

KINDS = [
    'casserole',
    'soup',
    'stew',
    'wok',
]


def generate_recipe_particle():
    food = ('{method} {food} {kind}'.format(
        method=(random.choice(METHODS) if random.random() < 0.5 else ''),
        food=random.choice(INGREDIENTS),
        kind=(random.choice(KINDS) if random.random() < 0.3 else ''),
    )).strip()
    if random.random() < 0.1:
        food = random.choice([
            '{name}\'s {food}',
            '{food} á la {name}',
        ]).format(
            name=fk.format('first_name'),
            food=food,
        )
    return food


RECIPE_NAME_GENERATORS = [
    lambda: generate_recipe_particle(),
    lambda: '{a} and {b}'.format(a=generate_recipe_particle(), b=generate_recipe_particle()),
    lambda: '{a} with {b}'.format(a=generate_recipe_particle(), b=generate_recipe_particle()),
]


def generate_recipe_name():
    name = random.choice(RECIPE_NAME_GENERATORS)()
    return name[0].upper() + name[1:]


def pick_creator():
    if random.random() < 0.3:
        return User.objects.order_by('?').first()


class RecipeFactory(DjangoModelFactory):
    ctime = fuzzy.FuzzyDateTime(
        start_dt=make_aware(datetime(2010, 1, 1)),
        end_dt=make_aware(datetime(2016, 1, 1)),
    )
    name = fuzzy.FuzzyAttribute(generate_recipe_name)
    content = Faker('text')
    creator = fuzzy.FuzzyAttribute(pick_creator)

    class Meta:
        model = Recipe

    @post_generation
    def clean(self, create, extracted, **kwargs):
        self.clean()

    @post_generation
    def ratings(self, create, extracted, **kwargs):
        for rater in User.objects.order_by('?')[:random.randint(0, 5)]:
            RecipeRating.objects.create(
                recipe=self,
                rater=rater,
                rating=random.randint(1, 6),
            )
