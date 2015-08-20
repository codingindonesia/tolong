# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_invitation'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='victim',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
