# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(null=True, blank=True)),
                ('reported_by', models.CharField(max_length=200, null=True, blank=True)),
                ('reported_date', models.DateTimeField(auto_now_add=True)),
                ('phone', models.CharField(max_length=200, null=True, blank=True)),
                ('email', models.CharField(max_length=200, null=True, blank=True)),
                ('location', models.CharField(max_length=400, null=True, blank=True)),
                ('longitude', models.CharField(max_length=220, null=True, blank=True)),
                ('latitude', models.CharField(max_length=220, null=True, blank=True)),
                ('has_response', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Responder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200, null=True, blank=True)),
                ('email', models.CharField(max_length=200, null=True, blank=True)),
                ('cell_phone', models.CharField(max_length=200, null=True, blank=True)),
                ('longitude', models.CharField(max_length=200, null=True, blank=True)),
                ('latitude', models.CharField(max_length=200, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('response_date', models.DateTimeField(auto_now_add=True)),
                ('response_report', models.TextField()),
                ('validity', models.IntegerField()),
                ('case_id', models.ForeignKey(to='service.Case')),
                ('responder', models.ForeignKey(to='service.Responder')),
            ],
        ),
    ]
