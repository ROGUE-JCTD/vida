# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('vida', '0013_auto_20160206_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personlocationhistory',
            name='person_uuid',
        ),
        migrations.AddField(
            model_name='personlocationhistory',
            name='person_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=1, to='vida.Person'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='personlocationhistory',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 7, 8, 47, 16, 873923)),
            preserve_default=False,
        ),
    ]
