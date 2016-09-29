import json

import pytest
from django.contrib.auth.models import User

from recipes.factories import RecipeFactory
from recipes.models import Recipe


@pytest.mark.django_db
def test_api(client):
    recipe = RecipeFactory(
        public=True,
        creator=User.objects.create_user(username='x')
    )
    assert isinstance(recipe, Recipe)
    data = json.loads(
        client.get(
            '/api/recipes/%d/' % recipe.pk,
        ).content.decode('utf8')
    )
    assert data['name'] == recipe.name
    assert data['creator']['id'] == recipe.creator_id
