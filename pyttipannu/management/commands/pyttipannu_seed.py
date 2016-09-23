from django.contrib.auth.models import User
from django.core.management import BaseCommand
from factory import DjangoModelFactory, fuzzy, Faker, post_generation


class UserFactory(DjangoModelFactory):
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    username = fuzzy.FuzzyText()

    @post_generation
    def _set_password(self, create, extracted, **kwargs):
        self.set_password('x')

    class Meta:
        model = User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username='admin', is_superuser=True).exists():
            User.objects.create_superuser(username='admin', password='admin')
            self.stdout.write('superuser admin/admin created')

        for x in range(15):
            user = UserFactory()
            self.stdout.write('created user %s' % user)
