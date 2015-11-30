# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vida', '0006_auto_20151123_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='date_of_birth',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='injury',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='nationality',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='phone_number',
            field=models.CharField(max_length=40, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='status',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
