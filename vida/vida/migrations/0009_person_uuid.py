# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vida', '0008_auto_20151209_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='uuid',
            field=models.CharField(default=b'None', max_length=100),
        ),
    ]
