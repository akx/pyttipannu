import pytest
import requests_mock

from recipes.kruoka_import import import_by_query
from recipes.tests.import_test_data import TEST_DATA


@pytest.mark.django_db
def test_importer():
    with requests_mock.mock() as m:
        m.post(
            'https://www.k-ruoka.fi/kr-api/search/pyttipannu?offset=0',
            json=TEST_DATA,
        )
        for recipe in import_by_query('pyttipannu'):
            assert recipe.name.endswith('K-Ruoka')
            assert 'pyttipannu' in recipe.name.lower()
            assert recipe.id
