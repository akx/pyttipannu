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


@pytest.mark.django_db
def test_auth_flow_splinter(settings, live_server, browser):
    """
    :type browser: splinter.driver.webdriver.BaseWebDriver
    """

    # Navigate home
    browser.visit(live_server.url)

    # Navigate to signup
    browser.find_by_text('Sign Up').click()

    # Post form
    username = get_random_string()
    password = get_random_string()
    browser.fill('username', username)
    browser.fill('password1', password)
    browser.fill('password2', password)
    browser.find_by_css('button[type=submit]').click()

    # See we got logged in
    assert browser.is_text_present(username)
    assert browser.is_text_present('Sign Out')

    # See we have an active user
    assert User.objects.filter(username=username, is_active=True).exists()
