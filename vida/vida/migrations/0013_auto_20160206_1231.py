# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('vida', '0012_auto_20160204_2031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personlocationhistory',
            name='person',
        ),
        migrations.RemoveField(
            model_name='personlocationhistory',
            name='shelter',
        ),
        migrations.AddField(
            model_name='personlocationhistory',
            name='person_uuid',
            field=models.CharField(default=b'None', max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='personlocationhistory',
            name='shelter_uuid',
            field=models.CharField(default=b'None', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='personlocationhistory',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
