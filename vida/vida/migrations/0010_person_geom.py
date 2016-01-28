# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vida', '0009_person_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(default=b'POINT(0.0 0.0)', srid=4326),
        ),
    ]
