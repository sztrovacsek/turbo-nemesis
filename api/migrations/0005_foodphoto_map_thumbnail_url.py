# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_foodphoto_feed_thumbnail_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodphoto',
            name='map_thumbnail_url',
            field=models.CharField(null=True, max_length=300, blank=True),
            preserve_default=True,
        ),
    ]
