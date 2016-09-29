import pytest
from django.contrib.auth.models import User


@pytest.fixture()
def staff_user(request):
    user = User.objects.create_user(
        username='teuvo',
        password='teuvo',
        is_staff=True,
    )

    def kill_dat_user():
        user.is_active = False
        user.save()
        print('i keeled le user :(')

    request.addfinalizer(kill_dat_user)
    return user


@pytest.mark.django_db
@pytest.mark.parametrize('user_fixture', ('staff_user', 'admin_user'))
def test_something_with_staff(request, user_fixture, random_recipe):
    user = request.getfuncargvalue(user_fixture)
    print(user.username, user.is_staff, user.is_superuser)
    random_recipe.creator = user
    random_recipe.save()
