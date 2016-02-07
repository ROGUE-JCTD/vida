# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vida', '0014_auto_20160207_0847'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonFieldHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_name', models.CharField(default=b'None', max_length=64)),
                ('old_value', models.CharField(max_length=128)),
                ('new_value', models.CharField(max_length=128)),
                ('date_of_change', models.DateTimeField()),
                ('changed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT)),
                ('person', models.ForeignKey(to='vida.Person', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
    ]
