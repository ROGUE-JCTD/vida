# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vida', '0004_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='shelter',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(default=b'POINT(0.0 0.0)', srid=4326),
        ),
    ]
