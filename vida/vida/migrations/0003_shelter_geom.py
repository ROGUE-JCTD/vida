# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vida', '0002_person_pic_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='shelter',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(default=b'SRID=4326;POINT(0 0)', srid=4326),
        ),
    ]
