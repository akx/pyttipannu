# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-23 10:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('mtime', models.DateTimeField(auto_now=True)),
                ('rating', models.IntegerField()),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='avg_rating',
            field=models.FloatField(db_index=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='rating_count',
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='public',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='reciperating',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='recipes.Recipe'),
        ),
        migrations.AlterUniqueTogether(
            name='reciperating',
            unique_together=set([('recipe', 'rater')]),
        ),
    ]
