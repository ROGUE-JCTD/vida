# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vida', '0010_person_geom'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonLocationHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(default=b'POINT(0.0 0.0)', srid=4326)),
                ('start_date', models.DateTimeField(null=True)),
                ('stop_date', models.DateTimeField(null=True)),
                ('person', models.ForeignKey(to='vida.Person', on_delete=django.db.models.deletion.PROTECT)),
                ('shelter', models.ForeignKey(to='vida.Shelter', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
    ]
