# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vida', '0002_person_site_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='race',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
