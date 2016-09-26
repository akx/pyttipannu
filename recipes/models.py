from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q
from django.db.models import Sum, Count
from django.db.models.signals import post_save
from django.shortcuts import resolve_url
from django.utils.text import slugify
from django.utils.six import python_2_unicode_compatible


class RecipeQuerySet(models.QuerySet):
    def public(self):
        return self.filter(public=True)

    def visible_to(self, user):
        q = Q(public=True)
        if user and user.is_authenticated():
            q |= (Q(public=False) & Q(creator=user))
        return self.filter(q)


@python_2_unicode_compatible
class Recipe(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    ctime = models.DateTimeField(auto_now_add=True, editable=False)
    mtime = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=128)
    public = models.BooleanField(db_index=True, default=False)
    avg_rating = models.FloatField(editable=False, db_index=True, null=True)
    rating_count = models.IntegerField(db_index=True, default=0)
    content = models.TextField()

    objects = RecipeQuerySet.as_manager()

    def get_absolute_url(self):
        return resolve_url('show', pk=self.pk, slug=slugify(self.name))

    def update_rating(self):
        rating_info = self.ratings.aggregate(
            sum=Sum('rating'),
            count=Count('*'),
        )
        self.rating_count = rating_info['count']
        if self.rating_count:
            self.avg_rating = rating_info['sum'] / self.rating_count
        else:
            self.avg_rating = None
        self.save(update_fields=('avg_rating', 'rating_count'))

    def __str__(self):
        return self.name

    def can_rate(self, user):
        return bool(user.is_authenticated)

    def can_edit(self, user):
        return (user and user.is_authenticated() and self.creator_id == user.id)

    def rate(self, user, rating):
        if not self.can_rate(user):
            raise PermissionDenied('can\'t rate')

        rating = int(rating)
        if not 1 <= rating <= 5:
            raise ValueError()
        self.ratings.update_or_create(
            rater=user,
            defaults={'rating': rating},
        )


class RecipeRating(models.Model):
    recipe = models.ForeignKey('Recipe', related_name='ratings')
    rater = models.ForeignKey(settings.AUTH_USER_MODEL)
    ctime = models.DateTimeField(auto_now_add=True, editable=False)
    mtime = models.DateTimeField(auto_now=True, editable=False)
    rating = models.IntegerField()

    class Meta:
        unique_together = [('recipe', 'rater'), ]


def update_recipe_rating(instance, **kwargs):
    instance.recipe.update_rating()


post_save.connect(update_recipe_rating, sender=RecipeRating)
