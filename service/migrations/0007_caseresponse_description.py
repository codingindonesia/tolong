# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_auto_20150821_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='caseresponse',
            name='description',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
