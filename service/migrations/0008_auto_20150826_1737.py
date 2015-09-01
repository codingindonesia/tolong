# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0007_caseresponse_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='reported_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='title',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
