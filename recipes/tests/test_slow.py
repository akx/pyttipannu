import time
from datetime import timedelta, datetime

from django.utils.timezone import now
from freezegun import freeze_time


def fun_function():
    time.sleep(10)
    return 810


def test_slow(monkeypatch):
    monkeypatch.setattr(time, 'sleep', lambda t: 0)

    assert fun_function() == 810


def is_account_expired(account_time):
    return (datetime.now() - account_time) > timedelta(days=5)


def test_time():

    account_time = datetime(2016, 1, 1, 18, 0, 0)
    with freeze_time('2016-01-02'):
        assert not is_account_expired(account_time)

    with freeze_time('2016-02-11'):
        assert is_account_expired(account_time)
