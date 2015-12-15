# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vida', '0007_auto_20151130_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='shelter',
            name='site_details',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='shelter_id',
            field=models.CharField(default=b'None', max_length=100, blank=True),
        ),
    ]
