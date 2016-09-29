import pytest
from django.contrib.auth.models import User

from recipes.factories import RecipeFactory
from recipes.models import Recipe, RecipeRating


@pytest.mark.django_db
@pytest.mark.parametrize('rating', (1, 3, 5))
@pytest.mark.parametrize('raters', (1, 5, 50))
def test_rating_gets_cached(request, raters, rating):
    recipe = RecipeFactory()
    assert isinstance(recipe, Recipe)
    assert recipe.rating_count == 0
    for x in range(raters):
        user = User.objects.create_user(username='%s' % x)
        recipe.rate(user, rating)
    recipe.refresh_from_db()
    assert recipe.rating_count == raters
    assert recipe.avg_rating == rating


@pytest.mark.django_db
def test_invalid_ratings_raise_exception():
    recipe = RecipeFactory()
    assert isinstance(recipe, Recipe)
    user = User.objects.create_user(username='s')
    with pytest.raises(ValueError):
        recipe.rate(user, 8)
