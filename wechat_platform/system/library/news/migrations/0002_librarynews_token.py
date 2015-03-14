# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='librarynews',
            name='token',
            field=models.CharField(default='', max_length=40, verbose_name='\u552f\u4e00\u6807\u8bc6\u7b26'),
            preserve_default=False,
        ),
    ]
