# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vida', '0011_personlocationhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='personlocationhistory',
            name='created_by',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='personlocationhistory',
            name='shelter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vida.Shelter', null=True),
        ),
    ]
