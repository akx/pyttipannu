import pytest

from recipes.factories import RecipeFactory


@pytest.fixture
def random_recipe():
    return RecipeFactory()
