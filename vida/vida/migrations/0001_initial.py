# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import django.db.models.deletion
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
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField(null=True)),
                ('stop_date', models.DateTimeField(null=True)),
                ('family_name', models.CharField(max_length=50, blank=True)),
                ('given_name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=20, blank=True)),
                ('age', models.CharField(max_length=10, blank=True)),
                ('mothers_given_name', models.CharField(max_length=50, blank=True)),
                ('fathers_given_name', models.CharField(max_length=50, blank=True)),
                ('date_of_birth', models.CharField(max_length=50, blank=True)),
                ('description', models.TextField(blank=True)),
                ('street_and_number', models.CharField(max_length=100, blank=True)),
                ('neighborhood', models.CharField(max_length=50, blank=True)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('province_or_state', models.CharField(max_length=50, blank=True)),
                ('phone_number', models.CharField(max_length=40, blank=True)),
                ('shelter_id', models.CharField(default=b'None', max_length=100, blank=True)),
                ('uuid', models.CharField(default=b'None', max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('barcode', models.CharField(max_length=100, null=True, blank=True)),
                ('injury', models.CharField(max_length=100, blank=True)),
                ('nationality', models.CharField(max_length=100, blank=True)),
                ('status', models.CharField(max_length=100, blank=True)),
                ('pic_filename', models.CharField(max_length=50, null=True, blank=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(default=b'POINT(0.0 0.0)', srid=4326)),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonFieldHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_name', models.CharField(default=b'None', max_length=64)),
                ('old_value', models.CharField(max_length=128)),
                ('new_value', models.CharField(max_length=128)),
                ('date_of_change', models.DateTimeField()),
                ('changed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT)),
                ('person', models.ForeignKey(to='vida.Person', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
        migrations.CreateModel(
            name='PersonLocationHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(default=b'POINT(0.0 0.0)', srid=4326)),
                ('start_date', models.DateTimeField()),
                ('stop_date', models.DateTimeField(null=True)),
                ('shelter_uuid', models.CharField(default=b'None', max_length=100, blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT)),
                ('person_id', models.ForeignKey(to='vida.Person', on_delete=django.db.models.deletion.PROTECT)),
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
                ('site_details', models.CharField(max_length=200, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(default=b'POINT(0.0 0.0)', srid=4326)),
                ('uuid', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
