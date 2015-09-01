# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_case_victim'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('cell_phone', models.CharField(max_length=200)),
                ('severity_level', models.IntegerField()),
                ('responded_date', models.DateTimeField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='case',
            options={'ordering': ['-reported_date']},
        ),
        migrations.AlterField(
            model_name='case',
            name='reported_date',
            field=models.DateTimeField(),
        ),
        migrations.AddField(
            model_name='caseresponse',
            name='case_id',
            field=models.ForeignKey(related_name='case_responses', to='service.Case'),
        ),
    ]
