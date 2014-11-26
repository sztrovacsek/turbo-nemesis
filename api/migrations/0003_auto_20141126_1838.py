# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_foodphoto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('description', models.TextField(blank=True, null=True)),
                ('foodphoto', models.ForeignKey(to='api.FoodPhoto')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='foodphoto',
            name='user',
            field=models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
