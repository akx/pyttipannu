import pytest
from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.utils.crypto import get_random_string


@pytest.mark.django_db
def test_auth_flow_client(settings, client):
    # Navigate home
    content = client.get('/').content
    assert b'Sign In' in content

    # Navigate to signup
    client.get(resolve_url('account_signup'))
    username = get_random_string()
    password = get_random_string()

    # Post form
    content = client.post(resolve_url('account_signup'), {
        'username': username,
        'password1': password,
        'password2': password,
    }, follow=True).content.decode('utf8')

    # See we got logged in
    assert username in content
    assert 'Sign Out' in content

    # See we have an active user
    assert User.objects.filter(username=username, is_active=True).exists()
