# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('official_account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('type', models.IntegerField(verbose_name='\u5a92\u4f53\u6587\u4ef6\u7c7b\u578b', choices=[(0, '\u666e\u901a\u5a92\u4f53\u6587\u4ef6'), (1, '\u56fe\u7247\u5a92\u4f53\u6587\u4ef6'), (2, '\u8bed\u97f3\u5a92\u4f53\u6587\u4ef6'), (3, '\u97f3\u4e50\u5a92\u4f53\u6587\u4ef6'), (4, '\u89c6\u9891\u5a92\u4f53\u6587\u4ef6')])),
                ('filename', models.CharField(max_length=50, verbose_name='\u6587\u4ef6\u540d')),
                ('extension', models.CharField(default=b'', max_length=10, verbose_name='\u6587\u4ef6\u6269\u5c55\u540d')),
                ('media', models.FileField(upload_to=b'media', verbose_name='\u5a92\u4f53\u6587\u4ef6')),
                ('size', models.IntegerField(default=0, verbose_name='\u6587\u4ef6\u5927\u5c0f')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('modified_datetime', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65f6\u95f4')),
                ('official_account', models.ForeignKey(verbose_name='\u6240\u5c5e\u516c\u4f17\u53f7', to='official_account.OfficialAccount')),
            ],
            options={
                'db_table': 'wechat_media',
                'verbose_name': '\u5a92\u4f53\u5b58\u50a8',
                'verbose_name_plural': '\u5a92\u4f53\u5b58\u50a8',
            },
            bases=(models.Model,),
        ),
    ]
