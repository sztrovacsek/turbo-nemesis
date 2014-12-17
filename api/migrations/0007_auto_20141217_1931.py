# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20141217_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='coords_x',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='coords_y',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
