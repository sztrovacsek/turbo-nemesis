# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_foodphoto_map_thumbnail_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='address_raw',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='coords_x',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='coords_y',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
