# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20150701_0530'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='suspect',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='response',
            name='severity_level',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
