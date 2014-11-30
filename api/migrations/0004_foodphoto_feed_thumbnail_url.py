# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20141126_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodphoto',
            name='feed_thumbnail_url',
            field=models.CharField(blank=True, max_length=300, null=True),
            preserve_default=True,
        ),
    ]
