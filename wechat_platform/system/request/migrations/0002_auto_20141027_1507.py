# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestmessage',
            name='msgid',
            field=models.BigIntegerField(serialize=False, verbose_name='\u6d88\u606fID', primary_key=True),
        ),
    ]
