# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('vida', '0015_personfieldhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 2, 9, 37, 16, 268868), auto_now_add=True),
            preserve_default=False,
        ),
    ]
