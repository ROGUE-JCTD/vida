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
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField(null=True)),
                ('stop_date', models.DateTimeField(null=True)),
                ('family_name', models.CharField(max_length=50, blank=True)),
                ('given_name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=10, blank=True)),
                ('age', models.CharField(max_length=10, blank=True)),
                ('mothers_given_name', models.CharField(max_length=50, blank=True)),
                ('fathers_given_name', models.CharField(max_length=50, blank=True)),
                ('description', models.TextField(blank=True)),
                ('street_and_number', models.CharField(max_length=100, blank=True)),
                ('neighborhood', models.CharField(max_length=50, blank=True)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('province_or_state', models.CharField(max_length=50, blank=True)),
                ('shelter', models.CharField(max_length=50, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('barcode', models.IntegerField(null=True, blank=True)),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shelter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50, blank=True)),
                ('description', models.TextField(blank=True)),
                ('street_and_number', models.CharField(max_length=100, blank=True)),
                ('neighborhood', models.CharField(max_length=50, blank=True)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('province_or_state', models.CharField(max_length=50, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
