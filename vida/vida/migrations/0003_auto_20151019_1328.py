# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vida', '0002_person_pic_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='barcode',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
