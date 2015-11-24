# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vida', '0005_auto_20151102_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='shelter',
        ),
        migrations.AddField(
            model_name='person',
            name='shelter_id',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='shelter',
            name='uuid',
            field=models.CharField(default='default', max_length=100),
            preserve_default=False,
        ),
    ]
