# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0002_auto_20141027_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestevent',
            name='raw',
            field=models.TextField(default=None, verbose_name='\u4fe1\u606f\u539f\u59cbXML\u5185\u5bb9'),
            preserve_default=False,
        ),
    ]
